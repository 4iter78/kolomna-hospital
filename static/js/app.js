/* ═══════════════════════════════════════════════
   app.js — общие JS-утилиты приложения
   ═══════════════════════════════════════════════ */

// ── Модальные окна ───────────────────────────────
function openModal(id) {
  document.getElementById(id || 'modal-create').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  document.getElementById(id || 'modal-create').classList.remove('open');
  document.body.style.overflow = '';
}

function closeOnOverlay(e, id) {
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
    const timeout = type === 'success'
        ? 2000
        : 10000;
    const container = document.getElementById('ajax-messages');

    const alert = document.createElement('div');

    const bsType = {
        success: 'success',
        error: 'danger',
        danger: 'danger',
        warning: 'warning',
        info: 'info'
    }[type] || 'success';

    alert.className = `alert alert-${bsType}`;
    alert.textContent = msg;

    container.prepend(alert);

    setTimeout(() => {
        alert.remove();
    }, timeout);
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
    const timeout = resp.success ? 2000 : 10000;
    showToast(
        resp.message,
        resp.success ? 'success' : 'danger'
    );
    setTimeout(function () { location.reload(); }, timeout);
})
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
        const timeout = resp.success ? 2000 : 10000;
        showToast(
            resp.message,
            resp.success ? 'success' : 'danger'
        );
        closeModal(modalId || 'modal-edit');
        setTimeout(function () { location.reload(); }, timeout);
    })
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

function exportVisibleRowsToExcel(
    tableSelector,
    fileName
) {

    const table =
        document.querySelector(tableSelector);

    if (!table) {
        console.error(
            `Таблица "${tableSelector}" не найдена`
        );
        return;
    }

    const exportColumns = [];

    // Всегда начинаем с № п/п
    const headers = ['№ п/п'];

    table.querySelectorAll('thead th')
        .forEach((th, index) => {

            if (
                th.dataset.export === 'false'
            ) {
                return;
            }

            exportColumns.push(index);

            headers.push(th.textContent.trim()
            );
        });

    const data = [headers];

    let rowNumber = 1;

    table.querySelectorAll(
        'tbody tr[data-id]'
    ).forEach(row => {

        if (row.style.display === 'none') {
            return;
        }

        const rowData = [rowNumber];

        exportColumns.forEach(index => {

            const cell =
                row.cells[index];

            rowData.push(
                cell
                    ? cell.textContent.trim()
                    : ''
            );
        });

        data.push(rowData);
        rowNumber++;
    });

    const ws =
        XLSX.utils.aoa_to_sheet(data);

    // Автоподбор ширины колонок
    const colWidths = [];
    data.forEach(row => {
        row.forEach((cell, index) => {
            const length =
                String(cell || '').length;
            if (!colWidths[index]) {
                colWidths[index] = {
                    wch: length
                };
            } else {
                colWidths[index].wch =
                    Math.max(
                        colWidths[index].wch,
                        length
                    );
            }
        });
    });

    colWidths.forEach(col => {
        col.wch = Math.min(
            col.wch + 3,
            50
        );
    });

    ws['!cols'] = colWidths;
    const wb =
        XLSX.utils.book_new();
    const sheetName =
        new Date()
            .toLocaleDateString('ru-RU')
            .replaceAll('.', '-');

    XLSX.utils.book_append_sheet(
        wb,
        ws,
        sheetName
    );

    XLSX.writeFile(
        wb,
        fileName ||
        `export_${sheetName}.xlsx`
    );
}
