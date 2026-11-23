// Base de la API. Como el frontend se sirve desde el mismo FastAPI, usamos ruta relativa.
const API = "";

// Definición de cada tabla: endpoint, campo de id, y campos del formulario.
const ENTIDADES = {
  productos: {
    endpoint: "/productos",
    idField: "id_prod",
    campos: [
      { name: "nombre", label: "Nombre", type: "text", required: true },
      { name: "precio", label: "Precio", type: "number", step: "0.01", required: true },
    ],
  },
  trabajadores: {
    endpoint: "/trabajadores",
    idField: "id",
    campos: [
      { name: "nombre", label: "Nombre", type: "text", required: true },
      { name: "telefono", label: "Teléfono", type: "text" },
      { name: "puesto", label: "Puesto", type: "text" },
    ],
  },
  platillos: {
    endpoint: "/platillos",
    idField: "id_plat",
    campos: [
      { name: "nombre", label: "Nombre", type: "text", required: true },
      { name: "precio", label: "Precio", type: "number", step: "0.01", required: true },
      { name: "id_prod", label: "Producto", type: "select-productos", required: true },
      { name: "id_trabajador", label: "Trabajador (opcional)", type: "select-trabajadores" },
    ],
  },
  inventario: {
    endpoint: "/inventario",
    idField: "id",
    campos: [
      { name: "id_prod", label: "Producto", type: "select-productos", required: true },
      { name: "cantidad", label: "Cantidad", type: "number", required: true },
    ],
  },
};

let cacheProductos = [];
let cacheTrabajadores = [];
let editando = null; // { tabla, id } o null si es creación

// ---------- Navegación de pestañas ----------
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById("panel-" + btn.dataset.tab).classList.add("active");
  });
});

// ---------- Carga inicial ----------
async function cargarTodo() {
  cacheProductos = await apiGet("/productos/");
  cacheTrabajadores = await apiGet("/trabajadores/");
  renderProductos();
  renderTrabajadores();
  renderPlatillos();
  renderInventario();
}

async function apiGet(path) {
  const res = await fetch(API + path);
  if (!res.ok) throw new Error("Error al cargar " + path);
  return res.json();
}

function nombreProducto(id) {
  const p = cacheProductos.find((p) => p.id_prod === id);
  return p ? p.nombre : `#${id}`;
}

function nombreTrabajador(id) {
  if (id === null || id === undefined) return "—";
  const t = cacheTrabajadores.find((t) => t.id === id);
  return t ? t.nombre : `#${id}`;
}

// ---------- Render de tablas ----------
function renderProductos() {
  const tbody = document.getElementById("tbody-productos");
  if (!cacheProductos.length) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="4">Aún no hay productos. Crea el primero.</td></tr>`;
    return;
  }
  tbody.innerHTML = cacheProductos
    .map(
      (p) => `
    <tr>
      <td>${p.id_prod}</td>
      <td>${esc(p.nombre)}</td>
      <td>$${Number(p.precio).toFixed(2)}</td>
      <td>${acciones("productos", p.id_prod)}</td>
    </tr>`
    )
    .join("");
}

function renderTrabajadores() {
  const tbody = document.getElementById("tbody-trabajadores");
  if (!cacheTrabajadores.length) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="5">Aún no hay trabajadores.</td></tr>`;
    return;
  }
  tbody.innerHTML = cacheTrabajadores
    .map(
      (t) => `
    <tr>
      <td>${t.id}</td>
      <td>${esc(t.nombre)}</td>
      <td>${esc(t.telefono || "—")}</td>
      <td>${esc(t.puesto || "—")}</td>
      <td>${acciones("trabajadores", t.id)}</td>
    </tr>`
    )
    .join("");
}

async function renderPlatillos() {
  const tbody = document.getElementById("tbody-platillos");
  const platillos = await apiGet("/platillos/");
  if (!platillos.length) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="6">Aún no hay platillos.</td></tr>`;
    return;
  }
  tbody.innerHTML = platillos
    .map(
      (pl) => `
    <tr>
      <td>${pl.id_plat}</td>
      <td>${esc(pl.nombre)}</td>
      <td>$${Number(pl.precio).toFixed(2)}</td>
      <td>${esc(nombreProducto(pl.id_prod))}</td>
      <td>${esc(nombreTrabajador(pl.id_trabajador))}</td>
      <td>${acciones("platillos", pl.id_plat)}</td>
    </tr>`
    )
    .join("");
}

async function renderInventario() {
  const tbody = document.getElementById("tbody-inventario");
  const inv = await apiGet("/inventario/");
  if (!inv.length) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="4">Aún no hay registros de inventario.</td></tr>`;
    return;
  }
  tbody.innerHTML = inv
    .map(
      (i) => `
    <tr>
      <td>${i.id}</td>
      <td>${esc(nombreProducto(i.id_prod))}</td>
      <td>${i.cantidad}</td>
      <td>${acciones("inventario", i.id)}</td>
    </tr>`
    )
    .join("");
}

function acciones(tabla, id) {
  return `
    <div class="row-actions">
      <button class="icon-btn" title="Editar" onclick="openForm('${tabla}', ${id})">✏️</button>
      <button class="icon-btn danger" title="Eliminar" onclick="eliminar('${tabla}', ${id})">🗑️</button>
    </div>`;
}

function esc(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ---------- Formulario modal (crear/editar) ----------
async function openForm(tabla, id = null) {
  editando = { tabla, id };
  const def = ENTIDADES[tabla];
  const form = document.getElementById("modal-form");
  const title = document.getElementById("modal-title");
  title.textContent = (id ? "Editar " : "Nuevo en ") + tabla;

  let registro = {};
  if (id !== null) {
    registro = await apiGet(`${def.endpoint}/${id}`);
  }

  form.innerHTML = def.campos
    .map((campo) => {
      const valor = registro[campo.name] ?? "";
      if (campo.type === "select-productos") {
        return `
          <div class="field">
            <label>${campo.label}</label>
            <select name="${campo.name}" ${campo.required ? "required" : ""}>
              <option value="">-- selecciona --</option>
              ${cacheProductos
                .map(
                  (p) =>
                    `<option value="${p.id_prod}" ${p.id_prod === valor ? "selected" : ""}>${esc(
                      p.nombre
                    )} (#${p.id_prod})</option>`
                )
                .join("")}
            </select>
          </div>`;
      }
      if (campo.type === "select-trabajadores") {
        return `
          <div class="field">
            <label>${campo.label}</label>
            <select name="${campo.name}">
              <option value="">-- ninguno --</option>
              ${cacheTrabajadores
                .map(
                  (t) =>
                    `<option value="${t.id}" ${t.id === valor ? "selected" : ""}>${esc(
                      t.nombre
                    )} (#${t.id})</option>`
                )
                .join("")}
            </select>
          </div>`;
      }
      return `
        <div class="field">
          <label>${campo.label}</label>
          <input name="${campo.name}" type="${campo.type}" ${campo.step ? `step="${campo.step}"` : ""} value="${valor}" ${campo.required ? "required" : ""} />
        </div>`;
    })
    .join("");

  document.getElementById("modal-overlay").classList.add("open");
}

function closeForm() {
  document.getElementById("modal-overlay").classList.remove("open");
  editando = null;
}

async function submitForm() {
  const { tabla, id } = editando;
  const def = ENTIDADES[tabla];
  const form = document.getElementById("modal-form");
  if (!form.reportValidity()) return;

  const data = new FormData(form);
  const body = {};
  def.campos.forEach((campo) => {
    let valor = data.get(campo.name);
    if (campo.type === "number") valor = valor === "" ? null : Number(valor);
    if (campo.type.startsWith("select") && valor === "") valor = null;
    else if (campo.type.startsWith("select")) valor = Number(valor);
    body[campo.name] = valor;
  });

  const url = id !== null ? `${def.endpoint}/${id}` : `${def.endpoint}/`;
  const method = id !== null ? "PUT" : "POST";

  try {
    const res = await fetch(API + url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "No se pudo guardar");
    }
    closeForm();
    mostrarToast("Guardado correctamente", "success");
    await cargarTodo();
  } catch (e) {
    mostrarToast(e.message, "error");
  }
}

async function eliminar(tabla, id) {
  if (!confirm("¿Eliminar este registro? Esta acción no se puede deshacer.")) return;
  const def = ENTIDADES[tabla];
  try {
    const res = await fetch(`${API}${def.endpoint}/${id}`, { method: "DELETE" });
    if (!res.ok && res.status !== 204) throw new Error("No se pudo eliminar");
    mostrarToast("Eliminado", "success");
    await cargarTodo();
  } catch (e) {
    mostrarToast(e.message, "error");
  }
}

function mostrarToast(msg, tipo) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.className = "toast show " + tipo;
  setTimeout(() => (toast.className = "toast"), 2500);
}

// Cerrar modal haciendo clic fuera de él
document.getElementById("modal-overlay").addEventListener("click", (e) => {
  if (e.target.id === "modal-overlay") closeForm();
});

cargarTodo().catch((e) => mostrarToast("No se pudo conectar a la API: " + e.message, "error"));
