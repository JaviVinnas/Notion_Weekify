--borramos tablas y tipos de datos previamente definidos
DROP TYPE if exists dia_semana cascade;
DROP TYPE if exists cuatri cascade;
DROP TYPE if exists curso cascade;
drop table if exists metadatos cascade;
drop table if exists profes cascade;
drop table if exists asignaturas cascade;
drop table if exists clases cascade;

--creamos tipos de datos que nos interesen
CREATE TYPE dia_semana AS ENUM ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes','Sabado','Domingo');
CREATE TYPE cuatri AS ENUM ('Primer', 'Segundo', 'Anual');
CREATE TYPE curso AS ENUM ('Tercero', 'Cuarto');

create table metadatos
(
    token_v2              varchar(200) not null primary key,
    tabla_asignaturas     varchar(150) not null,
    tabla_cosas_con_fecha varchar(150) not null,
    tabla_profesores      varchar(150) not null
);

create table profes
(
    notion_id char(36)    not null primary key,
    nombre    varchar(50) not null
);

create table asignaturas
(
    notion_id           char(36)     not null primary key,
    nombre_completo     varchar(100) not null,
    nombre_abreviado    varchar(50),
    curso               curso        not null default 'Tercero',
    cuatri              cuatri       not null default 'Segundo',
    numero_teoricas     int          not null default 0,
    numero_practicas    int          not null default 0,
    acabadas_teoricas   boolean      not null default false,
    acabadas_practicas  boolean      not null default false,
    profe_teoricas      char(36)              default null,
    profe_practicas     char(36)              default null,
    foreign key (profe_teoricas) references profes (notion_id) on delete restrict on update cascade,
    foreign key (profe_practicas) references profes (notion_id) on delete restrict on update cascade
);
create table clases
(
    dia_semana  dia_semana not null,
    asignatura  char(36)   not null,
    hora_inicio int        not null,
    hora_fin    int        not null,
    practica    bool       not null,
    presencial  bool       not null,
    ubicacion varchar(100),
    primary key (asignatura, dia_semana, hora_inicio),
    foreign key (asignatura) references asignaturas (notion_id) on delete restrict on update cascade
);

--introducimos datos de prueba
--
--

--primero los metadatos de tablas
insert into metadatos(token_v2, tabla_asignaturas, tabla_cosas_con_fecha, tabla_profesores)
VALUES ('010ff674c490e963913b565148ed697edfe8dfb95846b1abb0d2c7dcdbb11dd7245aac4b86ade9001d45a89f5e08bce0c01daf2cabaef4349df6c6bd2c1884069e7714cc8020247ed94eb49af1e7',
        'https://www.notion.so/4a1954c0edca41ed91cb2f1b647b0567?v=273b5898c4944737b3a6c2a96d36a295',
        'https://www.notion.so/7fc92bc2787243409d03f303b65b61c1?v=db8f9014f61f44b5bc0ccb0e844dabb3',
        'https://www.notion.so/2edc8e581ccb47d88c35f80d25101154?v=1dbf5a74662148e8a062b3b27f4620d7');
--segundo todos los profesores que tengamos
insert into profes(notion_id, nombre)
VALUES ('23f2c9ea-6866-4265-b5b8-8137b9ca2950', 'Manuel Mucientes Molina');
insert into profes(notion_id, nombre)
VALUES ('8d4087ce-6b6c-43ea-a147-8400487da8a0', 'Alejandro Catala Bolos');
insert into profes(notion_id, nombre)
VALUES ('d3f5cbad-cdab-4fde-9c07-8584b21966fc', 'Eduardo Sánchez Vila');
insert into profes(notion_id, nombre)
VALUES ('8b4e2312-fdce-4fda-8bab-c4cd9803558e', 'Francisco Santiago Argüello Pedreira');
insert into profes(notion_id, nombre)
VALUES ('f3a68ab6-7f8d-4d8e-8d81-32a8a1eea19f', 'Senén Barro Ameneiro');
insert into profes(notion_id, nombre)
VALUES ('506cd4ba-10bd-4c39-a89e-f98ff77ac976', 'Pablo García Tahoces');
insert into profes(notion_id, nombre)
VALUES ('68d58e80-0ea3-43f2-9131-2da7c155f29c', 'Alejandro José Tobar Quintanar');
insert into profes(notion_id, nombre)
VALUES ('9a440139-a5e1-4114-bf17-6c58cb89bc11', 'José A. Taboada González');
insert into profes(notion_id, nombre)
VALUES ('a21d864d-dd8c-49a9-8808-4f4f769d09fe', 'Julián Flores González');
insert into profes(notion_id, nombre)
VALUES ('6de668c9-8747-4d2b-9aa7-e6b16002c583', 'José M. Cotos Yáñez');
insert into profes(notion_id, nombre)
VALUES ('21ed33c8-cc65-4bb3-9c1f-bef94a0b379f', 'Joaquín A. Triñanes Fernández');
--después las asignaturas que tengamos
--> primero las que sepamos su a.k.a. y luego las demás
insert into asignaturas(notion_id, nombre_completo, nombre_abreviado, curso, cuatri, profe_teoricas, profe_practicas)
values ('31b1cabc-83e4-4155-98f8-b6dbe608580f', 'Diseño de aplicaciones web', 'DAW', 'Tercero', 'Primer',
        '506cd4ba-10bd-4c39-a89e-f98ff77ac976', 'd3f5cbad-cdab-4fde-9c07-8584b21966fc'),
       ('3b387c7a-1c6c-4908-981e-a31be6621c4b', 'Administración de sistemas y redes', 'ASR', 'Tercero', 'Primer',
        '8b4e2312-fdce-4fda-8bab-c4cd9803558e', '8b4e2312-fdce-4fda-8bab-c4cd9803558e'),
       ('76ef8d45-7e72-4859-87a0-98995e400029', 'Teoría de automatas y lenguajes formales', 'TALF', 'Tercero', 'Primer',
        'f3a68ab6-7f8d-4d8e-8d81-32a8a1eea19f', '23f2c9ea-6866-4265-b5b8-8137b9ca2950'),
       ('ecfa031e-534a-41a5-a652-431852cf1950', 'Ingeniería de software', 'ENSO', 'Tercero', 'Anual',
        '6de668c9-8747-4d2b-9aa7-e6b16002c583', '9a440139-a5e1-4114-bf17-6c58cb89bc11'),
       ('3da12d28-d148-4ebc-834c-96992483b3b9', 'Interaccion persona-ordenador', 'IPO', 'Tercero', 'Primer',
        '68d58e80-0ea3-43f2-9131-2da7c155f29c', '68d58e80-0ea3-43f2-9131-2da7c155f29c');

insert into asignaturas(notion_id, nombre_completo, curso, cuatri)
values ('49e2d68a-2c48-4848-ac15-e38eb5042f9f', 'Computación en la nube', 'Tercero', 'Segundo'),
       ('ef638a73-777f-4a1c-9d65-903b35e9f6c3', 'Gestión de recursos humanos y comportamiento organizacional',
        'Tercero', 'Segundo'),
       ('c0a0d38d-15ec-4236-bd9f-52c656238555', 'Ingeniería de servicios', 'Tercero', 'Segundo'),
       ('a7f4a221-3340-4854-b2e0-cdc7b4e12828', 'Ingeniería de computadores', 'Tercero', 'Segundo'),
       ('d4e3b574-df38-4d17-aefd-cff8634bc239', 'Computación distribuída', 'Tercero', 'Segundo');
--por último insertamos las clases (las del primer cuatri de tercero como demo)
insert into clases(dia_semana, asignatura, hora_inicio, hora_fin, practica, presencial, ubicacion)
values --lunes
       ('Lunes', 'ecfa031e-534a-41a5-a652-431852cf1950', 540, 600, false, false, null),
       ('Lunes', '31b1cabc-83e4-4155-98f8-b6dbe608580f', 600, 660, false, false, null),
       ('Lunes', '3da12d28-d148-4ebc-834c-96992483b3b9', 660, 720, false, false, null),
       ('Lunes', '31b1cabc-83e4-4155-98f8-b6dbe608580f', 930, 1050, true, true, 'Condesa Aula I8 sitio 5'),
       ('Lunes', '3da12d28-d148-4ebc-834c-96992483b3b9', 1050, 1170, true, true, 'Condesa Aula I8 sitio 11'),
       --martes
       ('Martes', 'ecfa031e-534a-41a5-a652-431852cf1950', 540, 600, false, false, null),
       ('Martes', '76ef8d45-7e72-4859-87a0-98995e400029', 600, 660, false, false, null),
       ('Martes', 'ecfa031e-534a-41a5-a652-431852cf1950', 690, 840, true, true, 'ETSE Aula I2 sitio 10'),
       ('Martes', '3b387c7a-1c6c-4908-981e-a31be6621c4b', 930, 1050, true, true, 'Condesa Aula I5 sitio 13'),
       ('Martes', '31b1cabc-83e4-4155-98f8-b6dbe608580f', 1050, 1170, true, true, 'Condesa Aula I6 sitio 5'),
       --miercoles
       ('Miercoles','76ef8d45-7e72-4859-87a0-98995e400029', 1080, 1200, true, true, 'ETSE Aula I4 sitio 4'),
       --jueves
       ('Jueves', '3b387c7a-1c6c-4908-981e-a31be6621c4b', 540, 600, false, false, null),
       ('Jueves', '76ef8d45-7e72-4859-87a0-98995e400029', 600, 660, false, false, null),
       ('Jueves', '76ef8d45-7e72-4859-87a0-98995e400029', 660, 720, false, false, null),
       ('Jueves', '3b387c7a-1c6c-4908-981e-a31be6621c4b', 1050, 1170, true, true, 'Condesa Aula I5 sitio 13'),
       --viernes
       ('Viernes', '3da12d28-d148-4ebc-834c-96992483b3b9', 690, 810, true, true, 'Condesa Aula I8 sitio 11');