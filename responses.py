from lxml import etree
from werkzeug import exceptions
from food import db
from models import Shops, MenuList, ItemList, User, CategoryTypes
from helpers import (
    response,
    dict_to_etree,
    multiple_root_nodes,
    get_restaurant,
    RepeatedElement,
    generate_random,
)


@response()
def inquiry_done(_):
    """The request a restaurant part.
    In the forms, it give us the telephone of the restaurant,
    name of the restaurant, and restaurant type.
    TODO: append to database"""

    return {}


@multiple_root_nodes()
def basket_reset(request):
    return {}


@multiple_root_nodes()
def basket_list(request):
    zip_code = request.args.get("areaCode")
    query = User.query.filter_by(zip_code=zip_code).first()
    price = 0

    # Subtract the amount of indices in the list by 2 to get the amount we have to range over
    num = len(query.basket)
    data = []

    for i in range(num):
        price = int(query.basket[i]["price"]) * int(query.basket[i]["qty"]) + price
        data.append(
            RepeatedElement(
                {
                    "basketNo": i,
                    "menuCode": 1,
                    "itemCode": 1,
                    "name": query.basket[i]["name"],
                    "price": query.basket[i]["price"],
                    "size": 1,
                    "isSoldout": 0,
                    "quantity": query.basket[i]["qty"],
                    "subTotalPrice": 1,
                    "Menu": {
                        "name": "Menu",
                        "lunchMenuList": {
                            "isLunchTimeMenu": 1,
                            "isOpen": 1,
                        },
                    },
                    "optionList": {
                        "testing": {
                            "info": "Here so everything works!",
                            "code": 1,
                            "type": 1,
                            "name": "WiiLink",
                            "list": {
                                "item_one": {
                                    "name": "Item One",
                                    "menuCode": 1,
                                    "itemCode": 1,
                                    "image": 1,
                                    "isSoldout": 0,
                                    "info": "Here so everything works!",
                                    "price": "5.99",
                                }
                            },
                        }
                    },
                }
            )
        )
    return {
        "basketPrice": price,
        "totalPrice": price,
        "Status": {"isOrder": 1, "messages": {"hey": "how are you?"}},
        "List": {"generic": data},
    }


@multiple_root_nodes()
def auth_key(_):
    return {
        "authKey": "lol",
    }


@multiple_root_nodes()
def item_one(request):
    menu_code = request.args.get("menuCode")
    item_code = request.args.get("itemCode")
    queried_food = ItemList.query.filter_by(item_code=item_code).first()

    return {
        "price": queried_food.price,
        "optionList": {
            "testing": {
                "info": queried_food.description,
                "code": 1,
                "type": 1,
                "name": queried_food.name,
                "list": {
                    "item_one": {
                        "name": queried_food.name,
                        "menuCode": menu_code,
                        "itemCode": item_code,
                        "image": queried_food.item_code,
                        "isSoldout": 0,
                        "info": queried_food.description,
                        "price": queried_food.price,
                    }
                },
            }
        },
    }


@multiple_root_nodes()
def item_list(request):
    menuCode = request.args.get("menuCode")
    queried_food = (
        ItemList.query.filter_by(menu_code=menuCode)
        .order_by(ItemList.item_code.asc())
        .all()
    )

    return_dict = {"Count": 0, "List": {}}

    for i, item in enumerate(queried_food):
        return_dict["Count"] = return_dict["Count"] + 1

        food_list = {
            "name": item.name,
            "item": {
                "menuCode": menuCode,
                "itemCode": item.item_code,
                "price": item.price,
                "info": item.description,
                "size": 1,
                "image": item.item_code,
                "isSoldout": 0,
                "sizeList": {
                    "itemCode": item.item_code,
                    "size": 1,
                    "price": item.price,
                    "isSoldout": 0,
                },
            },
        }

        return_dict["List"].update({f"container{i}": food_list})

    return return_dict


@multiple_root_nodes()
def menu_list(request):
    shopCode = request.args.get("shopCode")
    query = (
        MenuList.query.filter_by(shop_code=shopCode)
        .order_by(MenuList.menu_code.asc())
        .all()
    )
    data = []

    for menu in query:
        data.append(
            RepeatedElement(
                {
                    "menuCode": menu.menu_code,
                    "linkTitle": menu.title,
                    "enabledLink": 1,
                    "name": menu.title,
                    "info": menu.info,
                    "setNum": 0,
                    "lunchMenuList": {
                        "isLunchTimeMenu": 1,
                        "hour": {
                            "start": 1,
                            "end": 1,
                        },
                        "isOpen": 1,
                    },
                    "message": "Where does this show up?",
                }
            )
        )

    return {
        "response": {
            "menu": data,
            # Placeholder menu item so the rest can show
            "menu2": {
                "menuCode": 2,
                "linkTitle": "More food!",
                "enabledLink": 1,
                "name": "Amazing food",
                "info": "Screamingly delightful.",
                "setNum": 0,
                "lunchMenuList": {
                    "isLunchTimeMenu": 1,
                    "hour": {
                        "start": 1,
                        "end": 1,
                    },
                    "isOpen": 1,
                },
                "message": "Where does this show up?",
            },
        }
    }


@multiple_root_nodes()
def shop_one(request):
    shopCode = request.args.get("shopCode")
    query = Shops.query.filter_by(shop_code=shopCode).first()
    return {
        "response": {
            "categoryCode": f"{query.category_code.value:02}",
            "address": query.address,
            "attention": "",
            "amenity": query.amenity,
            "menuListCode": 1,
            "activate": "on",
            "waitTime": 1,
            "timeorder": 1,
            "tel": query.phone,
            "yoyakuMinDate": 1,
            "yoyakuMaxDate": 2,
            "paymentList": {"athing": "Fox Card"},
            "shopStatus": {
                "hours": {
                    "all": {
                        "message": query.message,
                    },
                    "today": {
                        "values": {
                            "start": "00:00:00",
                            "end": "24:59:59",
                            "holiday": "n",
                        }
                    },
                    "delivery": {
                        "values": {
                            "start": "00:00:00",
                            "end": "24:59:59",
                            "holiday": "n",
                        }
                    },
                    "holiday": {
                        "status": {
                            "isOpen": 1,
                        }
                    },
                },
                "selList": {"values": {"id": 1, "name": "test"}},
            },
            "interval": 1,
        },
        "recommendItemList": {
            "container0": {
                "menuCode": 1,
                "itemCode": 1,
                "name": "AAAA",
                "price": 1,
                "info": "Freshly charred",
                "size": 1,
                "image": 1,
                "isSoldout": 0,
                "sizeList": {
                    "itemCode": 1,
                    "name": "AAAA",
                    "price": 1,
                    "info": "Freshly charred",
                    "size": 1,
                    "image": 1,
                    "isSoldout": 0,
                },
            },
        },
    }


@response()
def shop_info(request):
    # Return a blank dict for now
    return {}


@response()
def shop_list(request):
    return category_list(request)


@response()
def document_template(request):
    return {
        "container0": {"contents": "no terms and conditions"},
        "container1": {"contents": "no seriously, stop trying"},
        "container2": {"contents": "the heck are you doing"},
    }


@response()
def area_list(request):
    if request.args.get("zipCode"):
        # Nintendo, for whatever reason, require a separate "selectedArea" element
        # as a root node within output.
        # This violates about every XML specification in existence.
        # I am reasonably certain there was a mistake as their function to
        # interpret nodes at levels accepts a parent node, to which they seem to
        # have passed passed NULL instead of response.
        #
        # We are not going to bother spending time to deal with this.
        @response()
        def area_list_only_segments():
            return {
                "areaList": {
                    "place": {
                        "segment": "segment title",
                        "list": {
                            "areaPlace": {"areaName": "place name", "areaCode": 2}
                        },
                    },
                },
                "areaCount": 1,
            }

        area_list_output = area_list_only_segments()

        selected_area = dict_to_etree("selectedArea", {"areaCode": 1})
        selected_area_output = etree.tostring(selected_area, pretty_print=True)

        return area_list_output + selected_area_output

    area_code = request.args.get("areaCode")
    if not area_code:
        # We expect either a zip code or an area code.
        return exceptions.BadRequest()

    if area_code == "0":
        # An area code of 0 is passed upon first search.
        return {
            "areaList": {
                "place": {
                    "segment": "segment title",
                    "list": {"areaPlace": {"areaName": "place name", "areaCode": 2}},
                },
            },
            "areaCount": 1,
        }

    if area_code == "2":
        # An area code of 0 is passed upon first search. All else is deterministic.
        # Assign the user a unique area code upon first launch of the channel
        zip_code = generate_random(11)

        data = User(
            zip_code=zip_code,
            basket=[],
        )

        db.session.add(data)
        db.session.commit()
        return {
            "areaList": {
                "place": {
                    "container0": "aaaa",
                    "segment": "area_title",
                    "list": {
                        "areaPlace": {
                            "areaName": "place one",
                            "areaCode": area_code,
                            "isNextArea": 0,
                            "display": 1,
                            "kanji1": "title",
                            "kanji2": "kanji2",
                            "kanji3": "two",
                            "kanji4": "three",
                        }
                    },
                },
            },
            "areaCount": 1,
        }

    return exceptions.NotFound()


def formulate_restaurant(category_id: CategoryTypes) -> dict:
    return {
        "LargeCategoryName": "Meal",
        "CategoryList": {
            "TestingCategory": {
                "CategoryCode": f"{category_id.value:02}",
                "ShopList": {"Shop": get_restaurant(category_id)},
            }
        },
    }


@multiple_root_nodes()
def category_list(_):
    return {
        "response": {
            "Pizza": formulate_restaurant(CategoryTypes.Pizza),
            "Bento": formulate_restaurant(CategoryTypes.Bento_Box),
            "Sushi": formulate_restaurant(CategoryTypes.Sushi),
            "Fish": formulate_restaurant(CategoryTypes.Fish),
            "Seafood": formulate_restaurant(CategoryTypes.Seafood),
            "American": formulate_restaurant(CategoryTypes.Western),
            "Fast": formulate_restaurant(CategoryTypes.Fast_Food),
            "Indian": formulate_restaurant(CategoryTypes.Curry),
            "Party": formulate_restaurant(CategoryTypes.Party_Food),
            "Drinks": formulate_restaurant(CategoryTypes.Drinks),
            "Other": formulate_restaurant(CategoryTypes.Others),
            "Placeholder": formulate_restaurant(CategoryTypes.Others),
        }
    }


@multiple_root_nodes()
def basket_add(request):
    zip_code = request.form.get("areaCode")
    item_code = request.form.get("itemCode")
    qty = request.form.get("quantity")

    query = User.query.filter_by(zip_code=zip_code).first()
    queried_food = ItemList.query.filter_by(item_code=item_code).first()

    # Append data to the database
    order: list = query.basket
    basket = order + [
        {"name": queried_food.name, "price": queried_food.price, "qty": qty}
    ]

    query.basket = basket
    db.session.commit()

    return {"sketch": True}


@multiple_root_nodes()
def validate_condition(_):
    return {}


@multiple_root_nodes()
def order_done(request):
    return {}
