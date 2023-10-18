CREATE TABLE "myapp_user" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "password" varchar(100) NOT NULL,
    "email" varchar(100) NOT NULL
);