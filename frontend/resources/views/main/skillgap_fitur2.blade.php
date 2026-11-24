@extends('base.app')

@section('header_title', 'Analisis Skill Gap')

@section('content')
    <p class="text-sm text-gray-600 mb-6">Skill yang dibutuhkan mayoritas alumni di suatu bidang, tetapi tidak disebut oleh sebagian responden.</p>

    @if (!empty($error))
        <p class="text-red-500">{{ $error }}</p>
    @elseif (empty($adaData))
        <p class="text-gray-500">Belum ada data. Silakan upload Excel terlebih dahulu.</p>
    @else
        {{-- catatan dari backend --}}
        @if ($catatan)
            <div class="mb-6 rounded-lg border-l-4 border-[#febb3d] bg-[#febb3d]/10 px-4 py-3 text-sm text-[#0F294A]">
                {{ $catatan }}
            </div>
        @endif

        @if (empty($adaDataGap))
            <p class="text-gray-500">
                Skill gap belum bisa dihitung. Backend hanya menghitungnya untuk bidang dengan minimal 5 responden.
            </p>
        @else
            <div class="space-y-8">

                {{-- 1. Ranking --}}
                <section class="rounded-lg border border-gray-200 p-5">
                    <h2 class="text-lg font-semibold text-[#0F294A] mb-1">Skill Paling Sering Tidak Disebut</h2>
                    <p class="text-sm text-gray-500 mb-4">Jumlah responden yang tidak menyebut skill ini, padahal dominan di bidangnya.</p>
                    <div class="relative w-full min-w-0 h-[360px]"><canvas id="chartRanking"></canvas></div>
                </section>

                {{-- 2. Dibutuhkan vs Tidak Disebut --}}
                <section class="rounded-lg border border-gray-200 p-5">
                    <h2 class="text-lg font-semibold text-[#0F294A] mb-1">Dibutuhkan vs Tidak Disebut</h2>
                    <p class="text-sm text-gray-500 mb-4">Perbandingan berapa kali skill disebut dan berapa kali absen.</p>
                    <div class="relative w-full min-w-0 h-[400px]"><canvas id="chartBanding"></canvas></div>
                </section>

                {{-- 3. Tren --}}
                <section class="rounded-lg border border-gray-200 p-5">
                    <h2 class="text-lg font-semibold text-[#0F294A] mb-1">Tren Antar Angkatan</h2>
                    <p class="text-sm text-gray-500 mb-4">
                        Angka 0 berarti skill tidak masuk 5 teratas pada angkatan itu, bukan berarti tidak pernah absen.
                    </p>
                    <div class="relative w-full min-w-0 h-[360px]"><canvas id="chartTren"></canvas></div>
                </section>

                {{-- 4. Waktu tunggu --}}
                <section class="rounded-lg border border-gray-200 p-5">
                    <h2 class="text-lg font-semibold text-[#0F294A] mb-1">Waktu Tunggu Kerja vs Skill Tidak Disebut</h2>
                    <p class="text-sm text-gray-500 mb-4">Rata-rata jumlah skill yang tidak disebut per responden, menurut lama menunggu pekerjaan pertama.</p>
                    <div class="relative w-full min-w-0 h-[300px]"><canvas id="chartWaktu"></canvas></div>
                </section>

            </div>

            <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
            <script>
                const BIRU = '#2B72D6', BIRU_TUA = '#1E3A8A', KUNING = '#febb3d';
                const TEKS = '#0F294A', ABU = '#6B7280', KISI = '#F3F4F6';
                const PALET = [BIRU_TUA, BIRU, KUNING, '#14B8A6', '#8B5CF6'];

                const horizontal = {
                    indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                    scales: {
                        x: { beginAtZero: true, ticks: { precision: 0, color: ABU }, grid: { color: KISI } },
                        y: { ticks: { color: TEKS, font: { size: 13 } }, grid: { display: false } }
                    }
                };

                // 1. Ranking
                new Chart(document.getElementById('chartRanking'), {
                    type: 'bar',
                    data: {
                        labels: @json(collect($ranking)->pluck('skill')),
                        datasets: [{
                            label: 'Responden',
                            data: @json(collect($ranking)->pluck('jumlah')),
                            backgroundColor: BIRU, hoverBackgroundColor: BIRU_TUA, borderRadius: 6
                        }]
                    },
                    options: { ...horizontal, plugins: { legend: { display: false } } }
                });

                // 2. Dibutuhkan vs tidak disebut
                new Chart(document.getElementById('chartBanding'), {
                    type: 'bar',
                    data: {
                        labels: @json(collect($banding)->pluck('skill')),
                        datasets: [
                            { label: 'Dibutuhkan', data: @json(collect($banding)->pluck('dibutuhkan')), backgroundColor: BIRU, borderRadius: 4 },
                            { label: 'Tidak Disebut', data: @json(collect($banding)->pluck('dirasa_kurang')), backgroundColor: KUNING, borderRadius: 4 }
                        ]
                    },
                    options: { ...horizontal, plugins: { legend: { position: 'top' } } }
                });

                // 3. Tren
                const trenSeries = @json($trenSeries);
                new Chart(document.getElementById('chartTren'), {
                    type: 'line',
                    data: {
                        labels: @json($angkatan),
                        datasets: trenSeries.map((s, i) => ({
                            label: s.skill, data: s.data,
                            borderColor: PALET[i % PALET.length],
                            backgroundColor: PALET[i % PALET.length],
                            tension: 0.3, pointRadius: 4
                        }))
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: { legend: { position: 'bottom' } },
                        scales: {
                            x: { ticks: { color: TEKS }, grid: { display: false } },
                            y: { beginAtZero: true, ticks: { precision: 0, color: ABU }, grid: { color: KISI } }
                        }
                    }
                });

                // 4. Waktu tunggu
                const waktuN = @json($waktuN);
                new Chart(document.getElementById('chartWaktu'), {
                    type: 'bar',
                    data: {
                        labels: @json($waktuLabels),
                        datasets: [{
                            label: 'Rata-rata skill tidak disebut',
                            data: @json($waktuAvg),
                            backgroundColor: BIRU, hoverBackgroundColor: BIRU_TUA, borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: { callbacks: { afterLabel: (c) => waktuN[c.dataIndex] + ' responden' } }
                        },
                        scales: {
                            x: { ticks: { color: TEKS }, grid: { display: false } },
                            y: { beginAtZero: true, ticks: { color: ABU }, grid: { color: KISI } }
                        }
                    }
                });
            </script>
        @endif
    @endif
@endsection