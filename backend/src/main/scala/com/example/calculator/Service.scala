package com.example.calculator

// json4s and jackson
import org.json4s.{ DefaultFormats, jackson }

// scala
import scala.concurrent.Future
import scala.concurrent.Await
import scala.concurrent.duration.Duration
import scala.concurrent.ExecutionContext

// akka
import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.server.Directives
import akka.stream.Materializer
import akka.http.scaladsl.client.RequestBuilding
import akka.http.scaladsl.model.{ HttpResponse, HttpRequest }
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.unmarshalling.Unmarshal
import akka.stream.scaladsl.{Flow, Sink, Source}

// java
import java.io.IOException


trait Service {

  def routes(implicit ec: ExecutionContext, mat: Materializer, system: ActorSystem) = {
    import Directives._
    import de.heikoseeberger.akkahttpjson4s.Json4sSupport._

    implicit val serialization = jackson.Serialization
    implicit val formats = DefaultFormats

    //val liveHost = "resttest.bench.co"
    //val livePort = 80
    
    val mockHost = "127.0.0.1"
    val mockPort = 8000

    val mockConnectionFlow: Flow[HttpRequest, HttpResponse, Any] =
      Http().outgoingConnection(host=mockHost, port=mockPort)

    def mockRequest(request: HttpRequest): Future[HttpResponse] = 
      Source.single(request).via(mockConnectionFlow).runWith(Sink.head)

    def fetchMockInfo(page: String)(implicit ec: ExecutionContext): Future[HttpResponse] = { 
      mockRequest(RequestBuilding.Get(s"/transactions/$page"))
    }

    def toCleanedRecord(result: Record): NormalizedRecord = {
      val company: String = result.Company.replaceAll("[^a-zA-Z0-9 /.]", "").split("x")(0).trim
      val format = new java.text.SimpleDateFormat("yyyy-MM-dd")
      NormalizedRecord(format.parse(result.Date), result.Ledger, result.Amount.toDouble, company)
    }

    def totalCountFuture(page: String): Future[Int]= {
      fetchMockInfo(page).flatMap { response =>
        response.status match {
          case OK => Unmarshal(response.entity).to[PageRecords].map{ jsonPage =>
            val futureTotal = jsonPage.totalCount
            futureTotal
          }
          case _ => Future.failed(new IOException("Mock IO error"))
        }
      }
    }

    def totalCount(page: String): Int = {
      val tcf = totalCountFuture(page)
      Await.result(tcf, Duration("1s"))
    }

    val itemsPerPage = 10

    def getTotalCount(page: String): Int = totalCount(page)/itemsPerPage + 1


    def getGroup(query: String): Future[List[NormalizedRecord]] = {
      fetchMockInfo(query).flatMap { response =>
        response.status match {
          case OK => Unmarshal(response.entity).to[PageRecords].map{ jsonPage =>
            val result = jsonPage.transactions.map(toCleanedRecord)
            result
          }
          case _ => Future.failed(new IOException("Mock IO error"))
        }
      }
    }

    def deDuped(page: String): Double = {
      val end = getTotalCount(page)
      val start = page.split('.')(0).toInt
      val records = for (i <- start to end) yield Await.result(getGroup(page), Duration("1s"))
      val flatted = records.flatten
      val deduped = flatted.toSet
      deduped.map(_.Amount).foldLeft(0.0)(_ + _)
    }

    def naive(page: String): Double = {
      val end = getTotalCount(page)
      val start = page.split('.')(0).toInt
      val records = for (i <- start to end) yield Await.result(getGroup(page), Duration("1s"))
      val flatted = records.flatten
      flatted.map(_.Amount).foldLeft(0.0)(_ + _)
    }

    logRequestResult("akka-http") {
      path("") {
        get {
          complete {
            <html>
              <body>
                <h2>Hello World!</h2>
              </body>
            </html>
          }
        }
      } ~
      path("totalBalanceDeDuped") {
        (post & path(Segment))
          entity(as[Page]) { jsonPage =>
          complete(Result(deDuped(jsonPage.page)))
        }
      } ~
      path("totalBalance") {
        (post & path(Segment))
          entity(as[Page]) { jsonPage =>
          complete(Result(naive(jsonPage.page)))
        }
      }
    }
  }
}