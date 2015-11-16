import sbt._
import Keys._

import spray.revolver.RevolverPlugin._

object ProjectBuild extends Build {
  lazy val root =
    Project("root", file("."))
      .aggregate(backend, mock)

  // Akka Http based backend
  lazy val backend =
    Project("backend", file("backend"))
      .settings(Revolver.settings: _*)
      .settings(commonSettings: _*)
      .settings(
        libraryDependencies ++= Seq(
          "com.typesafe.akka" %% "akka-http-experimental"               % "1.0",
          "com.typesafe.akka" %% "akka-http-spray-json-experimental"    % "1.0",
          "org.scala-lang"     % "scala-reflect"                        % "2.11.7",
          "com.typesafe.akka" %% "akka-slf4j"                           % "2.3.9",
          "de.heikoseeberger" %% "akka-http-json4s"                     % "1.1.0",
          "org.json4s"        %% "json4s-native"                        % "3.3.0",
          "org.json4s"        %% "json4s-jackson"                       % "3.3.0",
          "org.json4s"        %% "json4s-ext"                           % "3.3.0",
          "com.fasterxml.jackson.core" % "jackson-databind"             % "2.6.3",
          "com.fasterxml.jackson.core" % "jackson-core"                 % "2.6.3",
          "org.scalatest"     %% "scalatest"                            % "2.2.5" % "test"
        )
      )

  // akka Http based mock serving 1.json, 2.json etc
  lazy val mock =
    Project("mock", file("mock"))
      .settings(Revolver.settings: _*)
      .settings(commonSettings: _*)
      .settings(
        libraryDependencies ++= Seq(
          "io.spray" %% "spray-json" % "1.3.2",
          "com.typesafe.akka" %% "akka-http-experimental" % "1.0",
          "com.typesafe.akka" %% "akka-http-spray-json-experimental" % "1.0",
          "de.heikoseeberger" %% "akka-http-json4s" % "1.1.0",
          "org.scala-lang" % "scala-reflect" % "2.11.7"
        )
      )

  def commonSettings = Seq(
    scalaVersion := "2.11.7"
  ) //ScalariformSupport.formatSettings

  resolvers += "hseeberger at bintray" at "http://dl.bintray.com/hseeberger/maven"

}