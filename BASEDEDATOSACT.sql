CREATE DATABASE dissoft;
USE dissoft;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol_id INT, 
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha DATE NOT NULL,
    ubicacion VARCHAR(255) NOT NULL,
    organizador_id INT,
    resultado TEXT,
    FOREIGN KEY (organizador_id) REFERENCES usuarios(id)
);

CREATE TABLE asistentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actividad_id INT,
    usuario_id INT,
    FOREIGN KEY (actividad_id) REFERENCES actividades(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actividad_id INT, 
    descripcion TEXT, 
    FOREIGN KEY (actividad_id) REFERENCES actividades(id)
);

CREATE TABLE reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actividad_id INT,
    total_asistentes INT, 
    descripcion TEXT, 
    FOREIGN KEY (actividad_id) REFERENCES actividades(id)
);

INSERT INTO roles (nombre) VALUES ('Administrador');
INSERT INTO roles (nombre) VALUES ('Usuario');

INSERT INTO usuarios (nombre, email, contrasena, rol_id) 
VALUES ('Edwin Muniz', 'edwin@example.com', '123456', 1);

INSERT INTO usuarios (nombre, email, contrasena, rol_id) 
VALUES ('Ana Perez', 'ana@example.com', 'abcdef', 2);

SELECT u.id, u.nombre, u.email, r.nombre AS rol
FROM usuarios u
LEFT JOIN roles r ON u.rol_id = r.id;
