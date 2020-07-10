## Dress-as API

#### 0. General

- DEV API Domain (OLD): [Contact support for the domain]:4455

- DEV API Domain (NEW): [Contact support for the domain]:4460

#### 1. Authentication

##### 1.1 Login

- Description: This api is used for obtain the jwt token. Device_id is unique user device identifer, e.g. uuid / andriodid etc.

- Method: **POST**

- URL: ```/users/login```

- Body:

    ```json
    {
        "device_id": "string",
        "email": "string",
        "password": "string"
    }
    ```

- Response:

    **200**

    ```json
    {
        "user_id": 1,
        "account_type": "application / google",
        "token": "token"
    }
    ```

    **400**

    ```json
    {
        "error": "please provide email and password"
    }
    ```

    **403**

    ```json
    {
        "error": "incorrect email or password"
    }
    ```

##### 1.2 Logout

- Description: Expire the current login token.

- Method: **POST**

- URL: ```/users/logout/```

- Header: Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    {
        "token": null
    }
    ```

##### 1.3 Register

- Description: Register a new account with email, password and device id. 

- Method: **POST**

- URL: ```/users/register/```

- Body:

    ```json
    {
        "email": "string",
        "password": "password",
        "device_id": "string",
        "location": "string" (optional),
    }
    ```

- Response:

    **201**

    ```json
    {
        "user_id": ,
        "account_type": "application / google",
        "token": "jwt token"
    }
    ```

    **400**

    ```json
    {
        "error": "invalid email"
    }
    ```

    **400**

    ```json
    {
        "error": "email exists"
    }
    ```

    **403**

    ```json
    {
        "error": "cannot register"
    }
    ```

    **400**

    ```json
    {
        "error": "please provide email and password"
    }
    ```

    **400**

    ```json
    {
        "error": "password too short"
    }

##### 1.4 Signin with Google

- Description: sign in with google account

- Method: **POST**

- URL: ```/users/login/google```

- Body:

    ```json
    {
        "id_token": "id_token return from Google Auth SDK",
        "device_id": "string",
    }
    ```

- Response:

    **201**

    **400**

    ```json
    {
        "error": "please provide device id and google email and profile id"
    }
    ```

#### 2. Snaps

##### 2.1 Get snaps

- Method: **GET**

- URL: ```/snaps?filter={filter}offset={offset}&offset_id={offset_id}&limit={limit}&order={ASC|DESC}&orderby={creation|popularity}```

- Description:
    All query params are options
    filter: editorpick
    order by creation = order by snap id
    order by popularity = order by number of click
    offset_id = get snaps with snap_id less than offset_id
    limit = max. number of result items

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    ```json
    [
        {
            "snap_id": 20173,
            "user_id": 4247,
            "is_editor_pick": true,
            "image_path": "https://d3mj7xbhm30rhm.cloudfront.net/detailed/7/thanyaw_87781288_1052311465137925_8255764977516440123_n.jpg",
            "image_id": 7003,
            "image_x": 1080,
            "image_y": 1350,
            "creator_propic": "https://d3mj7xbhm30rhm.cloudfront.net/detailed/6/1585143075088.jpeg",
            "username": "suihalee44",
            "allow_product_search": "N",
            "has_products": "Y",
            "n_follower": 2,
            "n_favourite": 0,
            "n_comment": 0,
            "is_favourite": false,
            "is_following": false,
            "thumbnail_path": "https://d3mj7xbhm30rhm.cloudfront.net/thumbnails/936/1170/1585143075088.jpeg"
        },
        {
            "snap_id": 20174,
            "user_id": 4247,
            "is_editor_pick": true,
            "image_path": "https://d3mj7xbhm30rhm.cloudfront.net/detailed/7/thanyaw_87781288_1052311465137925_8255764977516440123_n.jpg",
            "image_id": 7003,
            "image_x": 1080,
            "image_y": 1350,
            "creator_propic": "https://d3mj7xbhm30rhm.cloudfront.net/detailed/6/1585143075088.jpeg",
            "username": "suihalee44",
            "allow_product_search": "N",
            "has_products": "Y",
            "n_follower": 2,
            "n_favourite": 0,
            "n_comment": 0,
            "is_favourite": false,
            "is_following": false,
            "thumbnail_path": "https://d3mj7xbhm30rhm.cloudfront.net/thumbnails/936/1170/1585143075088.jpeg"
        }
    ]
    ```

##### 2.2 Get single snap

- Method: **GET**

- URL: ```/snaps/{snap_id}```

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    {
        "snap_id": 7511,
        "user_id": 4891,
        "product_id": 6810,
        "is_editor_pick": true,
        "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/BBF43E59-815C-4667-9432-03B8499E97B8.jpeg",
        "image_id": 8395,
        "image_x": 1242,
        "image_y": 1900,
        "creator_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/AEF6DBA2-B829-4B15-98A6-EF97744FF5BE.jpeg",
        "username": "juliakassas",
        "allow_product_search": "N",
        "has_products": "N",
        "n_follower": 1,
        "n_favourite": 0,
        "n_comment": 0,
        "is_favourite": false,
        "is_following": false,
        "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/780/1193/detailed/8/BBF43E59-815C-4667-9432-03B8499E97B8.jpeg"
    }
    ```

    **400**

    ```json
    {
        "error": "please specify snap id"
    }
    ```

    **404**

    ```json
    {
        "error": "no such snap"
    }
    ```

##### 2.3 Create snaps

- Method: **POST**

- URL: ```/snaps```

- Header: Authorization: "Bearer {token}"

- Body:

    ```json
    {
        "snaps": 
            [
                {
                    "title": "title1",
                    "description": "description1",
                    "image_name": "sample-image1" (do not include extension),
                    "image_body": "{base64 encoded image}",
                    "ref_id": "string"
                },
                {
                    "title": "title2",
                    "description": "description2",
                    "image_name": "sample-image2" (do not include extension),
                    "image_body": "{base64 encoded image}",
                    "ref_id": "string"
                }
            ]
    }
    ```

- Response:

    **201**
    ```json
    {
        "results": [
            {
                "result": true/false,
                "error": "string" (return if result is false),
                "snap_id": "integer",
                "allow_product_search": "Y" / "N",
                "has_products": "Y" / "N",
                "ref_id": "string"
            },
            {
                "result": true/false,
                "error": "string" (return if result is false),
                "snap_id": "integer",
                "allow_product_search": "Y" / "N",
                "has_products": "Y" / "N",
                "ref_id": "string"
            }
        ]
    }
    ```

    **400**

    ```json
    {
        "error": "please provide request body"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

##### 2.4 Remove a snap


- Method: **DELETE**

- URL: ```/snaps/{id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **204**


    **400**

    ```json
    {
        "error": "please specify snap id"
    }
    ```

    **400**

    ```json
    {
        "error": "no such snap"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot remove snap/snap image"
    }
    ```

##### 2.5 Get products of a snap

- Method: **GET**

- URL: ```/snaps/{id}/products```

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    [
        {
            "snap_product_id": 1868,
            "snap_id": 20229,
            "product_name": "ASOS DESIGN Curve chino short",
            "product_link": "https://click.linksynergy.com/deeplink?id=i9c9XMixCYM&mid=35719&murl=https%3A%2F%2Fwww.asos.com%2Fus%2Fasos-curve%2Fasos-design-curve-chino-short%2Fprd%2F12313719%3Fclr%3Dstone%26colourWayId%3D16393242%26SearchQuery%3D%26cid%3D9263",
            "product_price": 29,
            "product_price_range": "LOW",
            "is_favourite": "N"
        },
        {
            "snap_product_id": 1863,
            "snap_id": 20229,
            "product_name": "Missguided faux leather shorts with paperbag waist in peach",
            "product_link": "https://click.linksynergy.com/deeplink?id=i9c9XMixCYM&mid=35719&murl=https%3A%2F%2Fwww.asos.com%2Fus%2Fmissguided%2Fmissguided-faux-leather-shorts-with-paperbag-waist-in-peach%2Fprd%2F12924534%3Fclr%3Dpeach%26colourWayId%3D16434289%26SearchQuery%3D%26cid%3D9263",
            "product_price": 38,
            "product_price_range": "LOW",
            "is_favourite": "N"
        },
    ]
    ```

    **400**

    ```json
    {
        "error": "please specify snap id"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot get snap gcs product"
    }
    ```

##### 2.7 Search Snaps

- Method: **GET**

- URL: ```/snaps/search?q={keyword}&offset={offset}&offset_id={offset_id}&limit={limit}&order={ASC|DESC}&orderby={creation|popularity}```

- Header: (optional)Authorization: "Bearer {token}"

- Description:
    All query params are options
    filter: editorpick
    order by creation = order by snap id
    order by popularity = order by number of click
    offset_id = get snaps with snap_id less than offset_id
    limit = max. number of result items

- Response:

    **200**

    ```json
    [
        {
            "snap_id": 2512,
            "user_id": 1824,
            "is_editor_pick": true,
            "product_id": 2260,
            "popularity": 24282,
            "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/2/01345BC1-DC03-4107-9C22-97C7F1D78855.jpeg",
            "image_id": 2875,
            "image_x": 2448,
            "image_y": 3264,
            "creator_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/2/44ACB8ED-843D-465A-B0D4-2FC857AEA12B.jpeg",
            "username": "Sophiesmay",
            "allow_product_search": "N",
            "has_products": "N",
            "n_follower": 57,
            "n_favourite": 35,
            "n_comment": 1,
            "is_favourite": false,
            "is_following": false,
            "product": "In Love with snake?",
            "full_description": "Love my new snake printed jacket?",
            "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/1468/1958/detailed/2/01345BC1-DC03-4107-9C22-97C7F1D78855.jpeg"
        },
        {
            "snap_id": 937,
            "user_id": 1076,
            "is_editor_pick": true,
            "product_id": 835,
            "popularity": 13467,
            "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/1/dscf2998.JPG",
            "image_id": 1121,
            "image_x": 1651,
            "image_y": 2934,
            "creator_propic": null,
            "username": "mmgigante",
            "allow_product_search": "N",
            "has_products": "N",
            "n_follower": 8,
            "n_favourite": 14,
            "n_comment": 3,
            "is_favourite": false,
            "is_following": false,
            "product": "Yellow Dress",
            "full_description": "Yellow Summer Dress",
            "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/990/1760/detailed/1/dscf2998.JPG"
        },
    ]

##### 2.8 Get comments of a snap

- Method: **GET**

- URL: ```/snaps/{id}/comment?offset={offset}&offset_id={offset_id}&limit={limit}```

- Description:
    All query params are options
    offset_id = get comments with post_id less than offset_id
    limit = max. number of result items

- Response:

    **200**

    ```json
    [
        {
            "post_id": 130,
            "name": "testuser3",
            "timestamp": 1593069800,
            "user_id": 3,
            "status": "A",
            "message": "comment20200312",
            "user_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/4315_1590151469727_lrte-aq5.png"
        }
    ]
    ```

    **400**

    ```json
    {
        "error": "please specify snap id"
    }
    ```

##### 2.9 Post a comment

- Method: **POST**

- URL: ```/snaps/{id}/comment```

- Header: Authorization: "Bearer {token}"

- Body:

    ```json
    {
        "message": "comment",
    }
    ```

- Response:

    **201**

    **400**

    ```json
    {
        "error": "please provide request body"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **400**

    ```json
    {
        "error": "no such snap"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot create comment"
    }
    ```

##### 2.10 Collect product link click information

- Method: **POST**

- URL: ```/gcsproducts/{gcs_productid}/click```

- Body:

    ```json
    {
        "snap_id": "snap id",
        "url": "the url being clicked",
        "ip": "ip address"
    }
    ```

##### 2.11 Get snap info after login

- Method: **POST**

- URL: ```/snaps/{snap_id}/info-after-login```

- Header: Authorization: "Bearer {token}"

- Body:

    ```json
    {
        "snap_id": 7621,
        "is_favourite": false,
        "is_following": false
    },
    {
        "snap_id": 7620,
        "is_favourite": false,
        "is_following": false
    }
    ```

#### 3. Users

##### 3.1 Get user

- Method: **GET**

- URL: ```/users/{id}/profile```

- Response:

    **200**

    ```json
    {
        "user_id": 3,
        "firstname": "John",
        "lastname": "Doe",
        "username": "testuser3",
        "bio": "Hi",
        "tagline": "tagline",
        "instagram_url": "testig",
        "facebook_url": "testig",
        "twitter_url": "testig",
        "youtube_url": "testig",
        "tiktok_url": "testig",
        "website_url": "testig",
        "location": "Hong Kong",
        "user_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/4315_1590151469727.png",
        "image_name": "4315_1590151469727.png",
        "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/350/350/detailed/8/4315_1590151469727.png",
        "n_follower": 0,
        "n_following": 3,
        "n_favourite": 0
    }
    ```

    **400**

    ```json
    {
        "error": "please specify user id"
    }
    ```

##### 3.2 Change password

- Method: **POST**

- URL: ```/users/{id}/password```

- Header: Authorization: "Bearer {token}"

- Body:

    ```json
    {
        "curr_password": "current",
        "new_password": "new"
    }
    ```

- Response:

    **200**

    **400**

    ```json
    {
        "error": "please provide request body"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot change password"
    }
    ```

##### 3.3 Update user profile

- Method: **PATCH**

- URL: ```/users/{id}/profile```

- Header: Authorization: "Bearer {token}"

- Body: 

    ```json
    {
        (optional)"firstname": "John",
        (optional)"lastname": "Doe",
        (optional)"username": "John Doe",
        (optional)"bio": "Hi",
        (optional)"tagline": "string",
        (optional)"location": "string",
        (optional)"instagram_url": "url",
        (optional)"facebook_url": "url",
        (optional)"twitter_url": "url",
        (optional)"website_url": "url",
        (optional)"youtube_url": "url",
        (optional)"tiktok_url": "url"
    }
    ```

- Response:

    **200**

    **400**

    ```json
    {
        "error": "please provide request body"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **400**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot edit"
    }
    ```

##### 3.4 Upload user profile pic

- Method: **POST**

- URL: ```/users/{id}/propic```

- Header: Authorization: "Bearer {token}"

- Body:

    ```json
    {
        "image_name": "example"(not include extension),
        "image_body": "{base64 encoded image}"
    }
    ```

- Response:

    **200**

    **400**

    ```json
    {
        "error": "please provide request body"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot upload pro pic"
    }
    ```

##### 3.5 Remove user profile pic

- Method: **DELETE**

- URL: ```/users/{id}/propic```

- Header: Authorization: "Bearer {token}"

- Response:

    **204**

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

##### 3.6 Count user follower and following

- Method: **GET**

- URL: ```/users/{id}/follow/count```

- Response:

    **200**

    ```json
    {
        "n_following": 0,
        "n_follower": 1
    }
    ```

##### 3.7 Get follower

- Method: **GET**

- URL: ```/users/{id}/follower?offset_id={offset_id}&offset={offset}&limit={limit}```

- Description:
    All query params are options
    offset_id = get follower with user id followed before offset_id
    limit = max. number of result items

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    {
        "follower": [
            {
                "user_id": 11,
                "timestamp": 1593054999,
                "username": "americanstyle",
                "location": null,
                "user_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/0/LOGO2_2.jpg",
                "is_followed": "N"
            }

        ],
        "n_follower": 0
    }
    ```

##### 3.8 Get following

- Method: **GET**

- URL: ```/users/{id}/following?offset_id={offset_id}&offset={offset}&limit={limit}```

- Description:
    All query params are options
    offset_id = get follower with user id followed before offset_id
    limit = max. number of result items

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    [
        {
            "user_id": 11,
            "timestamp": 1593054999,
            "username": "americanstyle",
            "location": null,
            "user_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/0/LOGO2_2.jpg",
            "is_followed": "N"
        }

    ]
    ```

##### 3.9 Follow a user

- Method: **POST**

- URL: ```/users/{id}/follow/{blogger_id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **201**

    **400**

    ```json
    {
        "error": "please specify id(s)"
    }
    ```

    **400**

    ```json
    {
        "error": "user id and blogger id cannot be same"
    }
    ```

    **400**

    ```json
    {
        "error": "followed already"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot follow"
    }
    ```

##### 3.10 Unfollow a User

- Method: **DELETE**

- URL: ```/users/{id}/follow/{blogger_id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **204**

    **400**

    ```json
    {
        "error": "please specify id(s)"
    }
    ```

    **400**

    ```json
    {
        "error": "user id and blogger id cannot be same"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "Unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot unfollow"
    }
    ```

##### 3.11 Get favourite snaps

- Method: **GET**

- URL: ```/users/{id}/favourite/snap?offset={offset}&offset_id={offset_id}&limit={limit}```

- Description:
    All query params are options
    offset_id = get snaps with snap id favorited before offset_id
    limit = max. number of result items

- Header: Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    [
        {
            "snap_id": 7511,
            "user_id": 4891,
            "is_editor_pick": true,
            "product_id": 6810,
            "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/BBF43E59-815C-4667-9432-03B8499E97B8.jpeg",
            "image_id": 8395,
            "image_x": 1242,
            "image_y": 1900,
            "creator_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/AEF6DBA2-B829-4B15-98A6-EF97744FF5BE.jpeg",
            "username": "juliakassas",
            "allow_product_search": "N",
            "has_products": "N",
            "n_follower": 1,
            "n_favourite": 1,
            "n_comment": 0,
            "is_favourite": true,
            "is_following": false,
            "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/780/1193/detailed/8/BBF43E59-815C-4667-9432-03B8499E97B8.jpeg"
        }
    ]
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "Unauthorized"
    }
    ```

##### 3.12 Add a snap to favourite

- Method: **POST**

- URL: ```/users/{id}/favourite/snap/{snap_id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **201**

    **400**

    ```json
    {
        "error": "added already"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot add snap to favourite"
    }
    ```

##### 3.13 Remove a snap from favourite

- Method: **DELETE**

- URL: ```/users/{id}/favourite/snap/{snap_id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **204**

    **400**

    ```json
    {
        "error": "no record found"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot remove snap favourite"
    }
    ```

##### 3.14 Get favourite products

- Method: **GET**

- URL: ```/users/{id}/favourite/product```

- Header: Authorization: "Bearer {token}"

- Response:

    **200**

    ```json
    [
        {
            "snap_product_id": 3,
            "snap_id": 7563,
            "product_name": "ASOS DESIGN square neck top in cream",
            "product_link": "https://www.asos.com/us/asos-design/asos-design-square-neck-top-in-cream/prd/13245920?clr=cream&colourWayId=16534721&SearchQuery=&cid=4169",
            "product_image": "https://images.asos-media.com/products/asos-design-square-neck-top-in-cream/13245920-1-cream?wid=1024",
            "product_price_range": "LOW",
            "brand_name": "ASOS DESIGN",
            "product_detail_category": "Top",
            "f_timestamp": 1593535079
        },
        {
            "snap_product_id": 5,
            "snap_id": 7563,
            "product_name": "Noisy May roll neck jersey top in white",
            "product_link": "https://www.asos.com/us/noisy-may/noisy-may-roll-neck-jersey-top-in-white/prd/12438247?clr=white&colourWayId=16430223&SearchQuery=&cid=4169",
            "product_image": "https://images.asos-media.com/products/noisy-may-roll-neck-jersey-top-in-white/12438247-1-white?wid=1024",
            "product_price_range": "LOW",
            "brand_name": null,
            "product_detail_category": null,
            "f_timestamp": 1593535075
        },
        {
            "snap_product_id": 2,
            "snap_id": 7563,
            "product_name": "Monki A-line check mini skirt with buttons in brown",
            "product_link": "https://www.asos.com/us/monki/monki-a-line-check-mini-skirt-with-buttons-in-brown/prd/13241176?clr=brown&colourWayId=16448091&SearchQuery=&cid=2639",
            "product_image": "https://images.asos-media.com/products/monki-a-line-check-mini-skirt-with-buttons-in-brown/13241176-1-brown?wid=1024",
            "product_price_range": "LOW",
            "brand_name": "Monki",
            "product_detail_category": "Mini skirt",
            "f_timestamp": 1593535066
        },
        {
            "snap_product_id": 1,
            "snap_id": 7563,
            "product_name": "New Look Tall check skirt in black pattern",
            "product_link": "https://www.asos.com/us/new-look-tall/new-look-tall-check-skirt-in-black-pattern/prd/13628885?clr=black-pattern&colourWayId=16552993&SearchQuery=&cid=2639",
            "product_image": "https://images.asos-media.com/products/new-look-tall-check-skirt-in-black-pattern/13628885-1-blackpattern?wid=1024",
            "product_price_range": "LOW",
            "brand_name": "New Look",
            "product_detail_category": "Tall skirt",
            "f_timestamp": 1593535062
        }
    ]
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "Unauthorized"
    }
    ```

##### 3.15 Add a snap product to favourite

- Method: **POST**

- URL: ```/users/{id}/favourite/product/{snap_product_id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **201**

    **400**

    ```json
    {
        "error": "added already"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot add snap product to favourite"
    }
    ```

##### 3.16 Remove a snap product from favourite

- Method: **DELETE**

- URL: ```/users/{id}/favourite/product/{snap_product_id}```

- Header: Authorization: "Bearer {token}"

- Response:

    **204**

    **400**

    ```json
    {
        "error": "no record found"
    }
    ```

    **401**

    ```json
    {
        "error": "please login"
    }
    ```

    **401**

    ```json
    {
        "error": "unauthorized"
    }
    ```

    **500**

    ```json
    {
        "error": "cannot remove snap product favourite"
    }
    ```

##### 3.17 Get snaps of a user

- Method: **GET**

- URL: ```/users/{id}/snaps?offset={offset}&offset_id={offset_id}&limit={limit}&order={ASC|DESC}&orderby={creation|popularity}```

- Header: (optional)Authorization: "Bearer {token}"

- Description:
    All query params are options
    filter: editorpick
    order by creation = order by snap id
    order by popularity = order by number of click
    offset_id = get snaps with snap_id less than offset_id
    limit = max. number of result items

- Response:

    **200**

    ```json
    [
        {
            "snap_id": 7626,
            "user_id": 3,
            "is_editor_pick": false,
            "product_id": 6921,
            "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/test_image_1593058369_hDSgc.jpeg",
            "image_id": 8555,
            "image_x": 1080,
            "image_y": 1347,
            "creator_propic": null,
            "username": "abcde12345",
            "allow_product_search": "Y",
            "has_products": "Y",
            "n_follower": 0,
            "n_favourite": 0,
            "n_comment": 0,
            "is_favourite": false,
            "is_following": false,
            "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/938/1170/detailed/8/test_image_1593058369_hDSgc.jpeg"
        },
        {
            "snap_id": 7623,
            "user_id": 3,
            "is_editor_pick": false,
            "product_id": 6916,
            "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/8/test_image_1593056653_HipIT.jpeg",
            "image_id": 8554,
            "image_x": 1080,
            "image_y": 1347,
            "creator_propic": null,
            "username": "abcde12345",
            "allow_product_search": "Y",
            "has_products": "Y",
            "n_follower": 0,
            "n_favourite": 0,
            "n_comment": 0,
            "is_favourite": false,
            "is_following": false,
            "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/938/1170/detailed/8/test_image_1593056653_HipIT.jpeg"
        }
    ]
    ```

##### 3.18 Search user

- Method: **GET**

- URL: ```/users/search?q={keyword}

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    ```json
    [
        {
            "user_id": 11,
            "username": "americanstyle",
            "location": null,
            "user_propic": "https://d11gzdcabvug5x.cloudfront.net/detailed/0/LOGO2_2.jpg",
            "is_followed": "N"
        }
    ]
    ```

##### 3.19 Forget password

- Method: **POST**

- URL: ```/users/recover```

- Body:

    ```json
    {
        "email": "string",
    }
    ```

- Response:

    **200**

    **400**

    ```json
    {
        "error": "please provide email"
    }
    ```

##### 3.20 Get number of likes of a user

- Method: **GET**

- URL: ```/users/{id}/likes```

- Response:

    **200**
    ```
    {
        "likes": "integer",
    }
    ```

##### 3.21 Report a user

- Method: **POST**

- URL: ```/users/report/```

- Body:

    ```json
    {
        "user_id": 1,  (User being reported)
        "report_type": 1|2|3 (1: Inappropriate; 2: Spam; 3: Others)
        (optional)"remark": "remark"
    }
    ```

- Response:
    **201**


##### 3.22 Check username exist or not

- Method: **GET**

- URL: ```/users/username-exists/{username}```

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    **200**
    ```json
    {
        "result": "boolean"
    }
    ```

##### 3.23 Get following users' snaps

- Method: **GET**

- URL: ```/users/{userid}/following/snaps```

- Header: (optional)Authorization: "Bearer {token}"

- Response:

    **200**
    ```json
    [
        {
            "snap_id": 100,
            "user_id": 10,
            "is_editor_pick": true,
            "product_id": 97,
            "image_path": "https://d11gzdcabvug5x.cloudfront.net/detailed/0/436FAFAF-0508-4CF0-885A-3B8C8290AF33.jpeg",
            "image_id": 122,
            "image_x": 2730,
            "image_y": 4096,
            "creator_propic": null,
            "username": "anikateller",
            "allow_product_search": "N",
            "has_products": "N",
            "n_follower": 7,
            "n_favourite": 4,
            "n_comment": 1,
            "is_favourite": false,
            "is_following": true,
            "thumbnail_path": "https://d11gzdcabvug5x.cloudfront.net/thumbnails/1638/2457/detailed/0/436FAFAF-0508-4CF0-885A-3B8C8290AF33.jpeg"
        }
    ]
    ```

#### 4. Miscellaneous

##### 4.1 Get privacy policy

- Method: **GET**

- URL: ```/privacy```

- Response:

    **200**

    ```json
    {
        "policy": "html snippet"
    }
    ```

##### 4.2 Get terms and condition

- Method: **GET**

- URL: ```/terms```

- Response:

    **200**

    ```json
    {
        "terms": "html snippet"
    }
    ```

##### 4.3 Get country list

- Method: **GET**

- URL: ```/countries```

- Response:

    **200**

    ```json
    {
        "countries": "array"
    }
    ```

##### 4.4 Get getstart background images

- Method: **GET**

- URL: ```/background```

- Response:

    **200**

    ```json
    {
        "background": {
            "left": "image url",
            "right": "image url"
        }
    }
    ```

##### 4.5 Get social media list

- Method: **GET**

- URL: ```/social-media```

- Response:

    **200**

    ```json
    {
        "platforms": "array of social media platforms"
    }
    ```
