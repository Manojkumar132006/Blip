import 'package:flutter/material.dart';
import 'package:stac/stac.dart';

var _url = 'http://192.168.1.2:8001';

void main() async{
  await Stac.initialize();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return StacApp(
      title: 'Flutter Demo',
      theme: StacTheme.fromJson(
        themeJson
      ),
      homeBuilder:(_) {
        return Stac.fromNetwork(context:context,request:StacNetworkRequest(
          url:_url,
          method:Method.get
          )
        );
        }
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('You have pushed the button this many times:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
Map<String, dynamic> themeJson = {
  "brightness": "light",
  "disabledColor": "#60FEF7FF",
  "fontFamily": "Handjet",
  "colorScheme": {
    "brightness": "light",
    "primary": "#6750a4",
    "onPrimary": "#FFFFFF",
    "secondary": "#615B6F",
    "onSecondary": "#FFFFFF",
    "surface": "#FEFBFF",
    "onSurface": "#1C1B1E",
    "background": "#FEFBFF",
    "onBackground": "#1C1B1E",
    "surfaceVariant": "#E6E0EA",
    "onSurfaceVariant": "#48454D",
    "error": "#AB2D25",
    "onError": "#FFFFFF",
    "success": "#27BA62",
    "onSuccess": "#FFFFFF"
  }
};