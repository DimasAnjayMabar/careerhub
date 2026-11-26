@extends('base.app')

@section('header_title', 'Master Data')

@section('content')

    <form id="upload-form" method="POST" action="{{ route('base.upload') }}"
        enctype="multipart/form-data" data-has-file="{{ $file ? '1' : '0' }}">
        @csrf
        <input type="file" id="file-input" name="file" accept=".xlsx,.xls" class="hidden">
    </form>

    <!-- teks sukses -->
    @if (session('success'))
        <div class="mb-5 rounded-lg border border-green-200 bg-green-50 p-3 text-sm text-green-700">
            {{ session('success') }}
        </div>
    @endif

    <!-- eror gagal upload -->
    @if ($errors->has('file'))
        <div class="mb-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
            {{ $errors->first('file') }}
        </div>
    @endif

    <!-- eror validasi di browser -->
    <div id="client-error" hidden
        class="mb-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
    </div>

    <!--  -->
    <!-- Data saat ini -->
    @if ($file)
        <div class="mb-6 flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between">
            <div class="flex min-w-0 items-center gap-4">
                <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-[#0F294A]">
                    <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Zm0 0v5h5" />
                    </svg>
                </div>
                <div class="min-w-0">
                    <p class="text-sm text-gray-500">Data saat ini</p>
                    <p class="truncate font-semibold text-[#0F294A]">{{ $file['filename'] }}</p>
                    <p class="text-sm text-gray-500">
                        Diupload {{ \Carbon\Carbon::parse($file['uploaded_at'])->format('d/m/Y H:i') }}
                        &middot; {{ number_format($file['total_rows']) }} baris
                    </p>
                </div>
            </div>

            <div class="flex shrink-0 items-center gap-2">
                <button type="button" data-upload-trigger
                    class="inline-flex shrink-0 items-center justify-center gap-2 rounded-lg bg-[#0F294A] px-4 py-2.5 text-sm font-medium text-white
                        transition hover:bg-[#16396a] focus:outline-none focus:ring-2 focus:ring-[#2B72D6]/40 disabled:cursor-not-allowed disabled:opacity-60">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M7 9l5-5 5 5M12 4v12" />
                    </svg>
                    <span data-upload-label>Ganti File</span>
                </button>

                <form id="delete-form" method="POST" action="{{ route('base.upload.destroy') }}">
                    @csrf
                    @method('DELETE')
                    <button type="button" id="delete-open"
                        class="rounded-lg border border-red-200 px-4 py-2.5 text-sm font-medium text-red-600 transition hover:bg-red-50">
                        Hapus
                    </button>
                </form>
            </div>
        
        </div>
    @else
        <!--  -->
        <!-- Data masih kosong -->
        <div class="border border-gray-200 rounded-xl flex flex-col items-center justify-center py-6 text-center mb-10">
            <div class="mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-[#0F294A] opacity-50">
                <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8l-5-5Zm0 0v5h5" />
                </svg>
            </div>
            <p class="text-sm font-medium text-[#0F294A] opacity-40">Belum ada data</p>
        </div>

        <!-- Upload -->
        <div class="mb-6 flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 bg-white px-6 py-14 text-center">
            <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-50 text-[#0F294A]">
                <svg class="h-7 w-7" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M7 9l5-5 5 5M12 4v12" />
                </svg>
            </div>
            <p class="font-semibold text-[#0F294A]">Upload</p>
            <p class="mt-1 max-w-sm text-sm text-gray-500">
                Upload file Excel (.xlsx atau .xls, maksimal 10 MB) untuk mulai melihat dan menggunakan data
            </p>
            <button type="button" data-upload-trigger
                class="mt-5 inline-flex items-center gap-2 rounded-lg bg-[#0F294A] px-4 py-2.5 text-sm font-medium text-white
                    transition hover:bg-[#16396a] focus:outline-none focus:ring-2 focus:ring-[#2B72D6]/40 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M7 9l5-5 5 5M12 4v12" />
                </svg>
                <span data-upload-label>Upload File</span>
            </button>
        </div>
    @endif


    <!-- Ringkasan hasil uploadnya -->
        <!-- hanya show kl pas upload -->
    @if (session('upload_summary'))
        @php $s = session('upload_summary'); @endphp
        <div class="mb-6 rounded-xl border border-gray-200 bg-white p-5">
            <h3 class="mb-4 font-semibold text-[#0F294A]">Ringkasan hasil upload</h3>

            <div class="grid grid-cols-3 gap-3 text-center">
                <div class="rounded-lg bg-gray-50 p-3">
                    <p class="text-xl font-semibold text-[#0F294A]">{{ $s['jumlah_baris'] ?? 0 }}</p>
                    <p class="text-xs text-gray-500">Baris di file</p>
                </div>
                <div class="rounded-lg bg-green-50 p-3">
                    <p class="text-xl font-semibold text-green-700">{{ $s['jumlah_diproses'] ?? 0 }}</p>
                    <p class="text-xs text-green-700/80">Berhasil diproses</p>
                </div>
                <div class="rounded-lg {{ ($s['jumlah_dilewati'] ?? 0) > 0 ? 'bg-amber-50' : 'bg-gray-50' }} p-3">
                    <p class="text-xl font-semibold {{ ($s['jumlah_dilewati'] ?? 0) > 0 ? 'text-amber-700' : 'text-[#0F294A]' }}">
                        {{ $s['jumlah_dilewati'] ?? 0 }}
                    </p>
                    <p class="text-xs {{ ($s['jumlah_dilewati'] ?? 0) > 0 ? 'text-amber-700/80' : 'text-gray-500' }}">Dilewati</p>
                </div>
            </div>

            @if (!empty($s['errors']))
                <details class="mt-4 text-sm">
                    <summary class="cursor-pointer font-medium text-amber-700">
                        Lihat baris yang dilewati ({{ count($s['errors']) }})
                    </summary>
                    <ul class="mt-2 list-disc space-y-1 pl-5 text-gray-600">
                        @foreach ($s['errors'] as $err)
                            <li>{{ $err }}</li>
                        @endforeach
                    </ul>
                </details>
            @endif
        </div>
    @endif


    <!--  -->
    <!-- Tabel datanya -->
    @if ($file)
        @php $fade = !$showAll && $total > $previewLimit; @endphp

        <div class="overflow-hidden rounded-xl border border-gray-200 bg-white mb-6">
            <div class="flex items-center justify-between gap-3 border-b border-gray-100 px-4 py-4">
                <div>
                    <h3 class="font-semibold text-[#0F294A] mb-1">Data Responden</h3>
                    <p class="text-sm text-gray-500">
                        @if ($showAll && $paginator)
                            Menampilkan {{ $paginator->firstItem() }}–{{ $paginator->lastItem() }} dari {{ number_format($total) }} data
                        @elseif ($fade)
                            Pratinjau {{ number_format($total) }} data
                        @else
                            Menampilkan {{ count($rows) }} dari {{ number_format($total) }} data
                        @endif
                    </p>
                </div>

                <!-- Button untuk menampilkan data singkat -->
                @if ($showAll)
                    <a href="{{ route('base.upload.index') }}"
                        class="text-sm font-medium text-[#2B72D6] hover:underline">Tampilkan Ringkas</a>
                @endif
            </div>

            <div class="relative">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-gray-50 text-gray-600">
                            <tr>
                                <th class="px-5 py-3 font-medium">No</th>
                                <th class="px-5 py-3 font-medium">Angkatan</th>
                                <th class="px-5 py-3 font-medium">Program Studi</th>
                                <th class="px-5 py-3 font-medium">Bidang Pekerjaan</th>
                                <th class="px-5 py-3 font-medium">Waktu Tunggu</th>
                                <th class="px-5 py-3 font-medium">Kesesuaian</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100 text-[#0F294A]">
                            @php $start = $paginator ? $paginator->firstItem() : 1; @endphp
                            @forelse ($rows as $i => $row)
                                @php
                                    $badge = match ($row['kesesuaian'] ?? '') {
                                        'sesuai'          => 'bg-green-50 text-green-700',
                                        'sebagian sesuai' => 'bg-amber-50 text-amber-600',
                                        default           => 'bg-red-50 text-red-600',
                                    };
                                @endphp
                                <tr class="hover:bg-gray-50/70">
                                    <td class="px-5 py-3 text-gray-500">{{ $start + $i }}</td>
                                    <td class="px-5 py-3">{{ $row['angkatan'] }}</td>
                                    <td class="px-5 py-3">{{ $row['prodi'] }}</td>
                                    <td class="px-5 py-3">{{ $row['bidang'] }}</td>
                                    <td class="px-5 py-3">{{ $row['waktu_tunggu'] }} bulan</td>
                                    <td class="px-5 py-3">
                                        <span class="rounded-full px-2.5 py-1 text-xs font-medium {{ $badge }}">
                                            {{ ucfirst($row['kesesuaian'] ?? '-') }}
                                        </span>
                                    </td>
                                </tr>
                            @empty
                                <tr>
                                    <td colspan="6" class="px-5 py-10 text-center text-gray-400">
                                        Tidak ada baris data yang berhasil diproses dari file ini
                                    </td>
                                </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>

                <!-- Show sedikit dan button show full -->
                @if ($fade)
                    <div class="pointer-events-none absolute inset-x-0 bottom-0 flex h-56 items-end justify-center
                                bg-gradient-to-t from-white via-white/80 to-transparent pb-6">
                        <a href="{{ route('base.upload.index', ['tampil' => 'semua']) }}"
                            class="pointer-events-auto inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-5 py-2.5
                                text-sm font-medium text-[#0F294A] shadow-sm transition
                                hover:border-[#2B72D6] hover:text-[#2B72D6]">
                            Tampilkan Semua ({{ number_format($total) }} data)
                            <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m6 9 6 6 6-6" />
                            </svg>
                        </a>
                    </div>
                @endif
            </div>


            <!-- Pagination -->
            @if ($showAll && $paginator && $paginator->hasPages())
                @php
                    $cur  = $paginator->currentPage();
                    $last = $paginator->lastPage();
                    $from = max(1, $cur - 2);
                    $to   = min($last, $cur + 2);
                    $btn  = 'inline-flex h-9 min-w-9 items-center justify-center rounded-lg border px-3 text-sm transition';
                @endphp
                <nav class="flex flex-wrap items-center justify-center gap-1 border-t border-gray-100 px-5 py-4" aria-label="Pagination">
                    @if ($paginator->onFirstPage())
                        <span class="{{ $btn }} cursor-not-allowed border-gray-200 text-gray-300">Sebelumnya</span>
                    @else
                        <a href="{{ $paginator->previousPageUrl() }}" class="{{ $btn }} border-gray-200 text-[#0F294A] hover:bg-gray-50">Sebelumnya</a>
                    @endif

                    @if ($from > 1)
                        <a href="{{ $paginator->url(1) }}" class="{{ $btn }} border-gray-200 text-[#0F294A] hover:bg-gray-50">1</a>
                        @if ($from > 2)
                            <span class="px-1 text-gray-400">…</span>
                        @endif
                    @endif

                    @for ($p = $from; $p <= $to; $p++)
                        @if ($p === $cur)
                            <span aria-current="page" class="{{ $btn }} border-[#0F294A] bg-[#0F294A] text-white">{{ $p }}</span>
                        @else
                            <a href="{{ $paginator->url($p) }}" class="{{ $btn }} border-gray-200 text-[#0F294A] hover:bg-gray-50">{{ $p }}</a>
                        @endif
                    @endfor

                    @if ($to < $last)
                        @if ($to < $last - 1)
                            <span class="px-1 text-gray-400">…</span>
                        @endif
                        <a href="{{ $paginator->url($last) }}" class="{{ $btn }} border-gray-200 text-[#0F294A] hover:bg-gray-50">{{ $last }}</a>
                    @endif

                    @if ($paginator->hasMorePages())
                        <a href="{{ $paginator->nextPageUrl() }}" class="{{ $btn }} border-gray-200 text-[#0F294A] hover:bg-gray-50">Berikutnya</a>
                    @else
                        <span class="{{ $btn }} cursor-not-allowed border-gray-200 text-gray-300">Berikutnya</span>
                    @endif
                </nav>
            @endif
        </div>
    @endif


    <!-- Konfirmasi buat ganti file -->
    <dialog id="replace-dialog" class="m-auto w-full max-w-md rounded-xl p-0 backdrop:bg-black/40">
        <div class="p-6">
            <h3 class="text-lg font-semibold text-[#0F294A]">Ganti file data?</h3>
            <p class="mt-2 text-sm text-gray-600">
                Data dari
                <span class="font-medium text-[#0F294A]">{{ $file['filename'] ?? '' }}</span>
                akan diganti dengan
                <span id="replace-new-name" class="font-medium text-[#0F294A]"></span>.
                Data lama tidak bisa dikembalikan
            </p>
            <div class="mt-6 flex justify-end gap-2">
                <button type="button" id="replace-cancel"
                    class="rounded-lg border border-gray-200 px-4 py-2 text-sm text-[#0F294A] hover:bg-gray-50">
                    Batal
                </button>
                <button type="button" id="replace-confirm"
                    class="rounded-lg bg-[#0F294A] px-4 py-2 text-sm font-medium text-white hover:bg-[#16396a]">
                    Ganti File
                </button>
            </div>
        </div>
    </dialog>

    @if ($file)
    <!-- Konfirmasi hapus data -->
        <dialog id="delete-dialog" class="m-auto w-full max-w-md rounded-xl p-0 backdrop:bg-black/40">
            <div class="p-6">
                <h3 class="text-lg font-semibold text-[#0F294A]">Hapus data?</h3>
                <p class="mt-2 text-sm text-gray-600">
                    Data dari
                    <span class="font-medium text-[#0F294A]">{{ $file['filename'] }}</span>
                    akan dihapus dan tidak bisa dikembalikan.
                </p>
                <div class="mt-6 flex justify-end gap-2">
                    <button type="button" id="delete-cancel"
                        class="rounded-lg border border-gray-200 px-4 py-2 text-sm text-[#0F294A] hover:bg-gray-50">
                        Batal
                    </button>
                    <button type="button" id="delete-confirm"
                        class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-60">
                        Hapus Data
                    </button>
                </div>
            </div>
        </dialog>
    @endif


    <script>
    // ===== GANTI FILE / UPLOAD =====
        (function () {
            const MAX_MB   = 10;
            const form     = document.getElementById('upload-form');
            const input    = document.getElementById('file-input');
            const dialog   = document.getElementById('replace-dialog');
            const newName  = document.getElementById('replace-new-name');
            const errBox   = document.getElementById('client-error');
            const triggers = document.querySelectorAll('[data-upload-trigger]');
            const hasFile  = form.dataset.hasFile === '1';
            let busy = false;

            function showError(msg) {
                errBox.textContent = msg;
                errBox.hidden = false;
            }

            function startUpload() {
                busy = true;
                triggers.forEach(function (btn) {
                    btn.disabled = true;
                    const label = btn.querySelector('[data-upload-label]');
                    if (label) label.textContent = 'Memproses...';
                });
                form.submit();
            }

            triggers.forEach(function (btn) {
                btn.addEventListener('click', function () {
                    if (!busy) input.click();
                });
            });

            input.addEventListener('change', function () {
                errBox.hidden = true;
                const f = input.files[0];
                if (!f) return;

                const ext = f.name.split('.').pop().toLowerCase();
                if (ext !== 'xlsx' && ext !== 'xls') {
                    showError('Format file harus .xlsx atau .xls.');
                    input.value = '';
                    return;
                }
                if (f.size > MAX_MB * 1024 * 1024) {
                    showError('Ukuran file maksimal ' + MAX_MB + ' MB.');
                    input.value = '';
                    return;
                }

                if (hasFile) {
                    newName.textContent = f.name;
                    dialog.showModal();
                } else {
                    startUpload();
                }
            });

            document.getElementById('replace-confirm').addEventListener('click', function () {
                dialog.close();
                startUpload();
            });

            document.getElementById('replace-cancel').addEventListener('click', function () {
                dialog.close();
                input.value = '';
            });

            // tombol Esc
            dialog.addEventListener('cancel', function () {
                input.value = '';
            });
        })();


        // hapus data
        (function () {
            const dialog = document.getElementById('delete-dialog');
            const form   = document.getElementById('delete-form');
            const open   = document.getElementById('delete-open');
            if (!dialog || !form || !open) return;  

            const confirmBtn = document.getElementById('delete-confirm');

            open.addEventListener('click', function () {
                dialog.showModal();
            });

            document.getElementById('delete-cancel').addEventListener('click', function () {
                dialog.close();
            });

            confirmBtn.addEventListener('click', function () {
                confirmBtn.disabled = true;
                confirmBtn.textContent = 'Menghapus...';
                form.submit();
            });
        })();
    </script>

@endsection