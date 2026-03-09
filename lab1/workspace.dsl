workspace {
    name "MeowMeowExpress"
    description "Сервис для доставки посылок"

    !identifiers hierarchical

    model {
        properties { 
            structurizr.groupSeparator "/"
            workspace_cmdb "cmdb_mnemonic"
            architect "Антон Синюков"
        }

        my_user = person "User" "" "person"

        email_service = softwareSystem "Email Service" "" "ext"

        my_system = softwareSystem "MeowMeowExpress"{

            user_db = container "User DB"{
                technology "PostgreSQL"
                tags "database" "postgres"
            }

            delivery_db = container "Delivery DB"{
                technology "PostgreSQL"
                tags "database" "postgres"
            }

            parcel_db = container "Parcel DB"{
                technology "MongoDB"
                tags "database" "mongo"
            }

            notification_topic = container "Notification Topic"{
                technology "Kafka"
                tags "kafka"
            }

            user_service = container "User Service" {
                technology "C++ userver"
                tags "userver"
            }

            parcel_service = container "Parcel Service" {
                technology "C++ userver"
                tags "userver"
            }

            delivery_service = container "Delivery Service" {
                technology "C++ userver"
                tags "userver"
            }

            notification_service = container "Notification Service" {
                technology "C++ userver"
                tags "userver"
            }

            main_service = container "Main Service" {
                technology "C++ userver"
                tags "userver"
            }

            main_service -> user_service "Регистрация и получение пользовательских данных" "REST/HTTPS"
            main_service -> parcel_service "Создание и получение информации о посылках" "REST/HTTPS"
            main_service -> delivery_service "Создание и получение информации о доставках" "REST/HTTPS"
            main_service -> notification_topic "Создание уведомлений" "TCP"

            user_service -> user_db "CRUD запросы данных пользователей" "SQL/TCP"
            parcel_service -> parcel_db "CRUD запросы данных о посылках" "MQL/TCP"
            delivery_service -> delivery_db "CRUD запросы данных о доставке" "SQL/TCP"
            notification_service -> notification_topic "Получение уведомлений" "TCP"
            notification_service -> email_service "Отправка уведомлений" "SMTP"
        }

        my_user -> my_system "Пользовательские флоу" "REST/HTTPS"
        my_user -> my_system.main_service

    }

    views {
        properties {
            plantuml.format     "svg"
            kroki.format        "svg"
            structurizr.sort created
            structurizr.tooltips true
        }

        themes default

        systemContext my_system {
            include *
            autoLayout
        }

        container my_system {
            include *
            autoLayout 
        }

        dynamic my_system "create_delivery" {
            description "Сценарий: оформление доставки"

            my_user -> my_system.main_service "Запрос на оформление доставки"

            my_system.main_service -> my_system.user_service "Получение данных отправителя и получателя"
            my_system.user_service -> my_system.user_db "SELECT данных об отправителе и получателе"
            my_system.user_db -> my_system.user_service "Данные отправителя и получателя"
            my_system.user_service -> my_system.main_service "Данные отправителя и получателя"

            my_system.main_service -> my_system.parcel_service "Получение данных о посылке"
            my_system.parcel_service -> my_system.parcel_db "SELECT данных о посылке"
            my_system.parcel_db -> my_system.parcel_service "Данные посылки"
            my_system.parcel_service -> my_system.main_service "Данные посылки"

            my_system.main_service -> my_system.delivery_service "Создание новой доставки"
            my_system.delivery_service -> my_system.delivery_db "INSERT данных о доставке"
            my_system.delivery_db -> my_system.delivery_service "Данные доставки"
            my_system.delivery_service -> my_system.main_service "Данные доставки"

            my_system.main_service -> my_user "200 ОК с данными доставки"

            my_system.main_service -> my_system.notification_topic "Создание уведомления о новом статусе доставки"
            my_system.notification_service -> my_system.notification_topic "Получение уведомления о новом статусе доставки"
            my_system.notification_service -> email_service "Отправка email уведомления"

            # без увеличения отступов стрелки склеиваются
            autoLayout bt 1000 500
        }

        styles {
            element "person" {
                shape Person
                background #08427B
                color #FFFFFF
            }
            element "database" {
                shape cylinder
            }
            element "mongo" {
                background #00ED64
                stroke #001E2B
                color #001E2B
            }
            element "postgres" {
                background #0064a5
                stroke  #FFFFFF
                color #FFFFFF
            }
            element "ext" {
                background #DDDDDD
                stroke  #151523
                color #151523
            }
            element "kafka" {
                shape pipe
            }
        }
    }
}
