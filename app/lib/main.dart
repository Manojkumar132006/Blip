import 'package:flutter/material.dart';
import 'package:stac/stac.dart';

var _url = 'http://192.168.1.2:8000/ui/';

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
      homeBuilder:(context) {
        return Stac.fromNetwork(context:context,request:StacNetworkRequest(
          url:'${_url}login',
          method:Method.get
          )
        );
      }
    );
  }
}


Map<String, dynamic> themeJson = {
  "brightness": "light",
  "disabledColor": "#60FEF7FF",
  "fontFamily": "poppins",
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