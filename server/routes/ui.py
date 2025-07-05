from fastapi import APIRouter

router = APIRouter(prefix="/ui", tags=["ui"])

@router.get("/login")
async def ui():
    return {
        "type": "scaffold",
        "appBar": {
        "type": "appBar",
        "title": {
            "type": "text",
            "data": "Text Field",
            "style": {
            "color": "#ffffff",
            "fontSize": 21
            }
        },
        "backgroundColor": "#4D00E9"
        },
        "backgroundColor": "#ffffff",
        "body": {
        "type": "singleChildScrollView",
        "child": {
            "type": "container",
            "padding": {
            "left": 12,
            "right": 12,
            "top": 12,
            "bottom": 12
            },
            "child": {
            "type": "column",
            "mainAxisAlignment": "center",
            "crossAxisAlignment": "center",
            "children": [
                {
                "type": "sizedBox",
                "height": 24
                },
                {
                "type": "textField",
                "maxLines": 1,
                "keyboardType": "text",
                "textInputAction": "done",
                "textAlign": "start",
                "textCapitalization": "none",
                "textDirection": "ltr",
                "textAlignVertical": "top",
                "obscureText": False,
                "cursorColor": "#FC3F1B",
                "style": {
                    "color": "#000000"
                },
                "decoration": {
                    "hintText": "What do people call you?",
                    "filled": True,
                    "icon": {
                    "type": "icon",
                    "iconType": "cupertino",
                    "icon": "person_solid",
                    "size": 24
                    },
                    "hintStyle": {
                    "color": "#797979"
                    },
                    "labelText": "Name*",
                    "fillColor": "#F2F2F2"
                },
                "readOnly": False,
                "enabled": True
                },
                {
                "type": "sizedBox",
                "height": 24
                },
                {
                "type": "textField",
                "maxLines": 1,
                "keyboardType": "text",
                "textInputAction": "done",
                "textAlign": "start",
                "textCapitalization": "none",
                "textDirection": "ltr",
                "textAlignVertical": "top",
                "obscureText": False,
                "cursorColor": "#FC3F1B",
                "style": {
                    "color": "#000000"
                },
                "decoration": {
                    "hintText": "Where can we reach you?",
                    "filled": True,
                    "icon": {
                    "type": "icon",
                    "iconType": "cupertino",
                    "icon": "phone_solid",
                    "size": 24
                    },
                    "hintStyle": {
                    "color": "#797979"
                    },
                    "labelText": "Phone number*",
                    "fillColor": "#F2F2F2"
                },
                "readOnly": False,
                "enabled": True
                },
                {
                "type": "sizedBox",
                "height": 24
                },
                {
                "type": "textField",
                "maxLines": 1,
                "keyboardType": "text",
                "textInputAction": "done",
                "textAlign": "start",
                "textCapitalization": "none",
                "textDirection": "ltr",
                "textAlignVertical": "top",
                "obscureText": False,
                "cursorColor": "#FC3F1B",
                "style": {
                    "color": "#000000"
                },
                "decoration": {
                    "hintText": "Your email address",
                    "filled": True,
                    "icon": {
                    "type": "icon",
                    "iconType": "material",
                    "icon": "email",
                    "size": 24
                    },
                    "hintStyle": {
                    "color": "#797979"
                    },
                    "labelText": "Email",
                    "fillColor": "#F2F2F2"
                },
                "readOnly": False,
                "enabled": True
                },
                {
                "type": "sizedBox",
                "height": 24
                },
                {
                "type": "sizedBox",
                "height": 100,
                "child": {
                    "type": "textField",
                    "expands": True,
                    "cursorColor": "#FC3F1B",
                    "style": {
                    "color": "#000000"
                    },
                    "decoration": {
                    "filled": True,
                    "hintStyle": {
                        "color": "#797979"
                    },
                    "labelText": "Life story",
                    "fillColor": "#F2F2F2"
                    },
                    "readOnly": False,
                    "enabled": True
                }
                },
                {
                "type": "sizedBox",
                "height": 24
                },
                {
                "type": "textField",
                "maxLines": 1,
                "keyboardType": "text",
                "textInputAction": "done",
                "textAlign": "start",
                "textCapitalization": "none",
                "textDirection": "ltr",
                "textAlignVertical": "top",
                "obscureText": True,
                "cursorColor": "#FC3F1B",
                "style": {
                    "color": "#000000"
                },
                "decoration": {
                    "filled": True,
                    "suffixIcon": {
                    "type": "icon",
                    "iconType": "cupertino",
                    "icon": "eye",
                    "size": 24
                    },
                    "hintStyle": {
                    "color": "#797979"
                    },
                    "labelText": "Password*",
                    "fillColor": "#F2F2F2"
                },
                "readOnly": False,
                "enabled": True
                },
                {
                "type": "sizedBox",
                "height": 24
                },
                {
                "type": "textField",
                "maxLines": 1,
                "keyboardType": "text",
                "textInputAction": "done",
                "textAlign": "start",
                "textCapitalization": "none",
                "textDirection": "ltr",
                "textAlignVertical": "top",
                "obscureText": True,
                "cursorColor": "#FC3F1B",
                "style": {
                    "color": "#000000"
                },
                "decoration": {
                    "filled": True,
                    "suffixIcon": {
                    "type": "icon",
                    "iconType": "cupertino",
                    "icon": "eye",
                    "size": 24
                    },
                    "hintStyle": {
                    "color": "#797979"
                    },
                    "labelText": "Re-type password*",
                    "fillColor": "#F2F2F2"
                },
                "readOnly": False,
                "enabled": True
                },
                {
                "type": "sizedBox",
                "height": 48
                },
                {
                "type": "elevatedButton",
                "child": {
                    "type": "text",
                    "data": "Submit"
                },
                "style": {
                    "backgroundColor": "#4D00E9",
                    "padding": {
                    "top": 8,
                    "left": 12,
                    "right": 12,
                    "bottom": 8
                    }
                },
                "onPressed": {}
                }
            ]
            }
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