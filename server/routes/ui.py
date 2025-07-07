from fastapi import APIRouter

router = APIRouter(prefix="/ui", tags=["ui"])


@router.get("/login")
async def ui():
    return {
    "type":  "scaffold",
    "body":  {
        "type":  "container",
        "padding":  {
            "top":  64.0,
            "bottom":  16.0,
            "left":  16.0,
            "right":  16.0
        },
        "width":  1000,
        "height":  1000,
        "decoration":  {
            "gradient":  {
                "type":  "linearGradient",
                "colors":  [
                    "#050714",
                    "#070916",
                    "#0D1c38",
                    "#122a4c",
                    "#24547a"
                ],
                "begin":  "topCenter",
                "end":  "bottomCenter",
                "stops":  [
                    0.2,
                    0.4,
                    0.6,
                    0.8,
                    1.0
                ]
            }
        },
        "child":  {
            "type":  "column",
            "mainAxisAlignment":  "start",
            "crossAxisAlignment":  "center",
            "children":  [
                {
                    "type":  "text",
                    "data":  "Blip",
                    "style":  {
                        "color":  "#FFFFFF",
                        "fontSize":  68.0
                    }
                },
                {
                    "type":  "sizedBox",
                    "height":  180
                },
                {
                    "type":  "text",
                    "textAlign":  "center",
                    "data":  "Your People are waiting. Log in and bring your social life offline.",
                    "style":  {
                        "color":  "#FFFFFF",
                        "fontSize":  32
                    }
                },
                {
                    "type":  "sizedBox",
                    "height":  55
                },
                {
                    "type":  "elevatedButton",
                    "onPressed":  {
                        
                    },
                    "style":  {
                        "backgroundColor":  "#FFFFFF",
                        "padding":  {
                            "top":  15,
                            "bottom":  15,
                            "left":  10,
                            "right":  10
                        },
                        "alignment":  "center",
                        "roundedRectangleBorder":  {
                            "borderRadius":  20
                        }
                    },
                    "autofocus":  False,
                    "clipBehavior":  "antiAlias",
                    "child":  {
                        "type":  "row",
                        "spacing":  12,
                        "children":  [
                            {
                                "type":  "image",
                                "src":  "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/768px-Google_%22G%22_logo.svg.png",
                                "width":  34
                            },
                            {
                                "type":  "text",
                                "data":  "Continue with Google",
                                "style":  {
                                    "color":  "#000000",
                                    "fontSize":  20
                                }
                            }
                        ]
                    }
                },
                {
                    "type":  "sizedBox",
                    "height":  115
                },
                {
                    "type":  "text",
                    "data":  "By continuing you agree to acknowledge the Privacy Policy and Terms of Service.",
                    "style":  {
                        "color":  "#FFFFFF",
                        "fontSize":  16
                    },
                    "textAlign":  "center"
                }
            ]
        }
    }
}




@router.get("/home")
async def home():
    return {
        "type": "scaffold",
        "appBar": {
            "type": "appBar",
            "title": {
                "type": "text",
                "data": "Home Page",
                "style": {
                    "color": "#ffffff",
                    "fontSize": 21
                }
            },
            "backgroundColor": "#4D00E9"
        },
        "backgroundColor": "#ffffff",
        "body": {
            "type": "center",
            "child": {
                "type": "text",
                "data": "Welcome to the Home Page!",
                "style": {
                    "color": "#000000",
                    "fontSize": 18
                }
            }
        }
    }