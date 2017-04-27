lazy val root = (project in file("."))
  .settings(
    name := "atc",
    scalaVersion := "2.11.8"
  )

libraryDependencies += "org.apache.httpcomponents" % "httpclient" % "4.5.3"
