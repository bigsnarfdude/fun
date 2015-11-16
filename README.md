# Mock JSON Data Server

```$ sbt
[info] Loading project definition from /fun/project
...
> mock/re-start
[info] Resolving jline#jline;2.12.1 ...
[info] Done updating.
[info] Compiling 1 Scala source to /fun/mock/target/scala-2.11/classes...
[info] Application mock not yet started
[info] Starting application mock in the background ...
mock Starting com.example.mock.Main.main()
[success] Total time: 12 s, completed 6-Nov-2015 3:14:51 PM
> mock Listening on: http://localhost:8000
```

# Backend API Server

```$ sbt
[info] Loading project definition from /fun/project
...
> backend/run
[info] Updating {file:/Users/antigen/Desktop/fun/}backend...
[info] Resolving jline#jline;2.12.1 ...
[info] Done updating.
[info] Compiling 4 Scala sources to /fun/backend/target/scala-2.11/classes...
[info] Running CalculatorApp
[DEBUG] [11/06/2015 15:17:25.605] [run-main-0] [EventStream(akka://default)] logger log1-Logging$DefaultLogger started
[DEBUG] [11/06/2015 15:17:25.606] [run-main-0] [EventStream(akka://default)] Default Loggers started
[DEBUG] [11/06/2015 15:17:25.659] [run-main-0] [EventStream(akka://default)] logger log1-Logging$DefaultLogger started
[DEBUG] [11/06/2015 15:17:25.659] [run-main-0] [EventStream(akka://default)] Default Loggers started
Hit ENTER to exit[DEBUG] [11/06/2015 15:17:27.281] [default-akka.actor.default-dispatcher-6] [akka://default/system/IO-TCP/selectors/$a/0] Successfully bound to /0:0:0:0:0:0:0:0:9000
```

# get API data

```POST 
localhost:9000/totalBalance
```

```
curl localhost:9000/totalBalanceDeDuped
```
