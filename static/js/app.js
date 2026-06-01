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
  const modal = document.getElementById(id);
  console.log(modal);
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
    .then(function (data) {
      showToast(data.message || 'Запись удалена', 'success');
      setTimeout(function () { location.reload(); }, 800);
    })
    .catch(function () { showToast('Ошибка при удалении', 'error'); });
}

// ── PUT через fetch ──────────────────────────────
function submitEdit(url, formId, modalId) {
  const form = document.getElementById(formId);
  const data = {};
  new FormData(form).forEach(function (v, k) { data[k] = v; });
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
