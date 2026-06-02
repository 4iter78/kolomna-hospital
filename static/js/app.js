/* ═══════════════════════════════════════════════
   app.js — общие JS-утилиты приложения
   ═══════════════════════════════════════════════ */

// ── Модальные окна ───────────────────────────────
function openModal(id) {
  document.getElementById(id || 'modal-create').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  console.log('closing', id);
  document.getElementById(id || 'modal-create').classList.remove('open');
  document.body.style.overflow = '';
}

function closeOnOverlay(e, id) {
  console.log('closing overlay', id);
  if (e.target === e.currentTarget) closeModal(id);
}

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.open').forEach(function (m) {
      m.classList.remove('open');
    });
    document.body.style.overflow = '';
  }
});

// ── Toast-уведомления ────────────────────────────
function showToast(msg, type) {
  const t = document.createElement('div');
  t.className = 'toast ' + (type || 'success');
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(function () { t.remove(); }, 3000);
}

// ── DELETE через fetch ───────────────────────────
function deleteRecord(url, id) {
  if (!confirm('Удалить запись #' + id + '?')) return;

  fetch(url + id, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' }
  })
    .then(function (r) { return r.json(); })
    .then(function (resp) {
      showToast(resp.message || 'Запись удалена', 'success');

      const modal = document.getElementById(modalId);
      console.log(modal);
      setTimeout(function () { location.reload(); }, 800);
    })
    .catch(function () { showToast('Ошибка при удалении', 'error');
      setTimeout(function () { location.reload(); }, 50);
    });
}

// ── PUT через fetch ──────────────────────────────
function submitEdit(url, formId, modalId) {
  const form = document.getElementById(formId);
  const data = {};
  const formData = new FormData(form);
    formData.forEach((v, k) => {
      if (k.endsWith('[]')) {
        const key = k.replace('[]', '');
        if (!data[key]) data[key] = [];
        data[key].push(v);
      } else {
        data[k] = v;
      }
    });
  const id = data.id;
  delete data.id;

  fetch(url + id, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
    .then(function (r) { return r.json(); })
    .then(function (resp) {
      showToast(resp.message || 'Запись обновлена', 'success');
      closeModal(modalId || 'modal-edit');

      const modal = document.getElementById(modalId);
      console.log(modal);
      setTimeout(function () { location.reload(); }, 800);
    })
    .catch(function () { showToast('Ошибка при сохранении', 'error'); });
}

let sortDirections = {};

function enableTableSorting() {

    document.querySelectorAll('.sortable')
        .forEach((th, index) => {

            th.addEventListener('click', () => {
                sortTable(th, index);
            });

        });
}

function sortTable(th, columnIndex) {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(
        tbody.querySelectorAll('tr')
    );
    const key =
        `${table.id || 'table'}-${columnIndex}`;
    sortDirections[key] =
        !sortDirections[key];
    const asc = sortDirections[key];
    rows.sort((a, b) => {
        let aVal =
            a.cells[columnIndex]
                .innerText.trim();
        let bVal =
            b.cells[columnIndex]
                .innerText.trim();
        const numA = Number(aVal);
        const numB = Number(bVal);
        if (!isNaN(numA) && !isNaN(numB)) {
            return asc
                ? numA - numB
                : numB - numA;
        }
        return asc
            ? aVal.localeCompare(bVal, 'ru')
            : bVal.localeCompare(aVal, 'ru');
    });
    rows.forEach(row =>
        tbody.appendChild(row)
    );
}
document.addEventListener(
    'DOMContentLoaded',
    enableTableSorting
);

function initNameFilter() {

    const filter =
        document.getElementById('filter-name');

    if (!filter)
        return;

    filter.addEventListener(
        'input',
        applyNameFilter
    );

    applyNameFilter();
}

function applyNameFilter() {

    const name =
        document.getElementById('filter-name')
            .value
            .toLowerCase();

    let visibleCount = 0;

    document.querySelectorAll(
        '.table tbody > tr[data-id]'
    ).forEach(row => {

        const rowName =
            (row.dataset.name || '')
                .toLowerCase();

        const visible =
            !name ||
            rowName.includes(name);

        row.style.display =
            visible ? '' : 'none';

        if (visible) {
            visibleCount++;
        }
    });

    const counter =
        document.getElementById(
            'record-count'
        );

    if (counter) {
        counter.textContent =
            `Записей: ${visibleCount}`;
    }
}

function resetNameFilter() {

    const filter =
        document.getElementById(
            'filter-name'
        );

    if (filter) {
        filter.value = '';
    }

    applyNameFilter();
}

document.addEventListener(
    'DOMContentLoaded',
    () => {

        document
            .querySelectorAll('.table-filter')
            .forEach(filter => {

                filter.addEventListener(
                    'input',
                    applyTableFilters
                );

                filter.addEventListener(
                    'change',
                    applyTableFilters
                );

            });

    }
);

function applyTableFilters() {
    let visibleCount = 0;
    document.querySelectorAll(
        '.table tbody tr[data-id]'
    ).forEach(row => {
        let visible = true;
        console.log("apply filters", row)
        console.log("dataset", row.dataset)
        document
            .querySelectorAll('.table-filter')
            .forEach(filter => {
                if (!visible) {
                    return;
                }
                const field =
                    filter.dataset.filterField;
                const value =
                    filter.value.trim();
                if (!value) {
                    return;
                }
                if (field == 'id') {
                    const rowValue = row.dataset[field];
                    if (String(rowValue) !== String(value)) {
                        visible = false;
                    }
                    return;
                }
                // диапазон ОТ
                if (field.endsWith('_from')) {
                    const rowField =
                        field.replace('_from', '');
                    const rowValue =
                        row.dataset[rowField];
                    if (
                        rowValue &&
                        new Date(rowValue) <
                            new Date(value)
                    ) {
                        visible = false;
                    }
                    return;
                }
                // диапазон ДО
                if (field.endsWith('_to')) {
                    const rowField =
                        field.replace('_to', '');
                    const rowValue =
                        row.dataset[rowField];
                    if (
                        rowValue &&
                        new Date(rowValue) >
                            new Date(value)
                    ) {
                        visible = false;
                    }
                    return;
                }
                // обычный текстовый фильтр
                const rowValue =
                    (row.dataset[field] || '')
                        .toLowerCase();
                if (
                    !rowValue.includes(
                        value.toLowerCase()
                    )
                ) {
                    visible = false;
                }
            });
        row.style.display =
            visible ? '' : 'none';
        if (visible) {
            visibleCount++;
        }
    });
    const counter =
        document.getElementById(
            'record-count'
        );
    if (counter) {
        counter.textContent =
            `Записей: ${visibleCount}`;
    }
}

function resetTableFilters() {
    document
        .querySelectorAll('.table-filter')
        .forEach(filter => {
            filter.value = '';
        });
    applyTableFilters();
}

document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('.sidebar-nav');

    if (!nav) return;

    // Восстановление позиции
    const savedPosition = sessionStorage.getItem('sidebarScrollPosition');
    if (savedPosition !== null) {
        nav.scrollTop = parseInt(savedPosition, 10);
    }

    // Сохранение при прокрутке
    nav.addEventListener('scroll', function() {
        sessionStorage.setItem(
            'sidebarScrollPosition',
            nav.scrollTop
        );
    });
});
