package com.example

import org.scalatest._
import org.scalatest.concurrent._
import akka.http.scaladsl.model._

import akka.actor.ActorSystem
import akka.event.{LoggingAdapter, Logging}
import akka.http.scaladsl.Http
import akka.http.scaladsl.client.RequestBuilding
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import akka.http.scaladsl.marshalling.ToResponseMarshallable
import akka.http.scaladsl.model.{HttpResponse, HttpRequest}
import akka.http.scaladsl.model.StatusCodes._
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.unmarshalling.Unmarshal
import akka.stream.{ActorMaterializer, Materializer}
import akka.stream.scaladsl.{Flow, Sink, Source}
import scala.concurrent.{ExecutionContextExecutor, Future}
import spray.json.DefaultJsonProtocol
import com.example.calculator.AkkaHttpApp

class AppSpec extends FlatSpec with Matchers with ScalaFutures with BeforeAndAfterAll {

  implicit val testSystem = akka.actor.ActorSystem("test-system")
  import testSystem.dispatcher
  implicit val materializer = ActorMaterializer()
  val server = AkkaHttpApp.main(Array("akka-http"))

  override def afterAll = testSystem.shutdown()

  val connectionFlow: Flow[HttpRequest, HttpResponse, Future[Http.OutgoingConnection]] =
    Http().outgoingConnection(host="localhost", port=9000)
  
  val responseFuture: Future[HttpResponse] =
    Source.single(HttpRequest(uri = "/"))
      .via(connectionFlow)
      .runWith(Sink.head)

  "The app" should "return index.html on a GET to /" in {
    whenReady(responseFuture) { response =>
      whenReady(Unmarshal(response.entity).to[String]) { str =>
        str should include("Hello World!")
      }
    }
  }
}