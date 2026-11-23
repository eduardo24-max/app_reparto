-- Kraken Rolls — Esquema de base de datos (SQLite)
-- Las mismas tablas se crean automáticamente al correr la app (SQLAlchemy),
-- este script es por si se necesita crearlas manualmente en un gestor de BD.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS productos (
    id_prod INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre  VARCHAR(100) NOT NULL,
    precio  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS trabajadores (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre   VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    puesto   VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS platillos (
    id_plat       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        VARCHAR(100) NOT NULL,
    precio        REAL NOT NULL,
    id_prod       INTEGER NOT NULL,
    id_trabajador INTEGER,
    FOREIGN KEY (id_prod) REFERENCES productos (id_prod) ON DELETE CASCADE,
    FOREIGN KEY (id_trabajador) REFERENCES trabajadores (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS inventario (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    id_prod  INTEGER NOT NULL,
    cantidad INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (id_prod) REFERENCES productos (id_prod) ON DELETE CASCADE
);

-- Datos de ejemplo (opcional)
INSERT INTO productos (nombre, precio) VALUES
    ('Salmón fresco', 120.00),
    ('Camarón tempura', 95.00),
    ('Alga nori', 15.00);

INSERT INTO trabajadores (nombre, telefono, puesto) VALUES
    ('Ana López', '618-111-2233', 'Sushiman'),
    ('Luis Pérez', '618-222-3344', 'Repartidor');

INSERT INTO platillos (nombre, precio, id_prod, id_trabajador) VALUES
    ('Kraken Roll', 180.00, 1, 1),
    ('Tempura Roll', 150.00, 2, 1);

INSERT INTO inventario (id_prod, cantidad) VALUES
    (1, 30),
    (2, 20),
    (3, 100);
