# iAnimeServer
the server based on flask

DDL (MySQL)

1.  
     
        create database iAnimeSQL2

2.      
        use iAnimeSQL2

3. 

        create table user(
        id int not null auto_increment,
        phone char(11) not null,
        password varchar(100) not null,
        primary key(id)
        )default charset=utf8;
   
4. 

       create table information(
       user_id int not null,
       nick_name varchar(50) default 'NickName',
       avatar varchar(50) default 'Avatar',
       background_photo varchar(50) default 'BackgroundPhoto',
       signature varchar(50) default 'Signature',
       rank int default 1,
       primary key(user_id)
       )default charset=utf8;

5. 
        create table follow(
        user_id int not null,
        follower_id int not null,
        primary key(user_id, follower_id)
        )default charset=utf8;
        
6. 
        create table work(
        id bigint not null,
        artist int not null,
        artist_name varchar(50),
        name varchar(50),
        created bigint not null,
        description varchar(100),
        forks int default 0,
        likes int default 0,
        allow_download boolean default false,
        allow_sketch boolean default false,
        allow_fork boolean default false,
        primary key(id, artist, created)
        )default charset=utf8;
        
7.
        create table address (
        work_id bigint not null,
        path varchar(50) not null,
        original_image varchar(50),
        colorization_image varchar(50),
        user_id int not null,
        receipt varchar(50),
        primary key(work_id, user_id)
        )default charset=utf8;
        
8.
        create table my_like(
        user_id int not null,
        work_id bigint not null,
        primary key(user_id, work_id)
        )default charset=utf8;

