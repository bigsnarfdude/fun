package com.example.mock

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

trait MockApp {

  implicit val system = ActorSystem("mock")
  implicit val executor = system.dispatcher
  implicit val materializer = ActorMaterializer()
  sys.addShutdownHook({ system.shutdown() })
  

  val route =
    pathPrefix("transactions") {
      getFromResourceDirectory("data")
    }

  println("Listening on: http://localhost:8000")
  Http().bindAndHandle(route, interface="localhost", port=8000)

}

object Main extends App with MockApp {

}