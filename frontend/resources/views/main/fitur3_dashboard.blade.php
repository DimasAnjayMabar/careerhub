@extends('base.fitur3')

@section('dashboard-content')

    @if ($error)
        <p class="text-red-500">{{ $error }}</p>

    @else
        @php
            // Data KPI
            $totalResponden = $kpi['total_responden'] ?? 0;
            $rataWaktu = $kpi['avg_waktu_tunggu_bulan'] ?? 0;
            $persenSesuai = $kpi['persen_sesuai'] ?? 0;
            $persenSebagian = $kpi['persen_sebagian'] ?? 0;
            $persenTidak = $kpi['persen_tidak'] ?? 0;

            // Data distribusi bidang pekerjaan
            $bidangLabels = collect($distribusiBidang)
                ->pluck('bidang')
                ->values();

            $bidangJumlah = collect($distribusiBidang)
                ->pluck('jumlah')
                ->values();

            // Data distribusi waktu tunggu
            $waktuLabels = collect($distribusiWaktu)
                ->pluck('range')
                ->values();

            $waktuJumlah = collect($distribusiWaktu)
                ->pluck('jumlah')
                ->values();

            // Data kesesuaian kerja vs prodi
            $prodiLabels = collect($kesesuaianProdi)
                ->pluck('prodi')
                ->values();

            $sesuaiData = collect($kesesuaianProdi)
                ->map(fn($row) => $row['sesuai'] ?? 0)
                ->values();

            $sebagianData = collect($kesesuaianProdi)
                ->map(fn($row) => $row['sebagian sesuai'] ?? 0)
                ->values();

            $tidakData = collect($kesesuaianProdi)
                ->map(fn($row) => $row['tidak sesuai'] ?? 0)
                ->values();
        @endphp

        <!-- Dropdown Filter Global -->
        <div class="border border-gray-200 rounded-lg p-6 mb-10">
            <div class="flex gap-2.5 mb-8">
                <svg class="w-8 h-8 shrink-0" fill="none" stroke="#0F294A" stroke-width="1" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
                </svg>

                <span class="text-[#0F294A] text-xl font-semibold">Filter Global</span>
            </div>

            <form method="GET">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Filter Angkatan -->
                    <div class="mb-4">
                        <label for="angkatan"
                            class="block text-sm font-medium text-gray-600 mb-2">
                            Pilih Angkatan
                        </label>

                        <div class="relative">
                            <select name="angkatan" id="angkatan" onchange="this.form.submit()"
                                class="appearance-none w-full bg-gray-100 text-[#0F294A] px-4 py-2.5 pr-12 rounded-lg border border-transparent cursor-pointer transition
                                    hover:bg-gray-200/70
                                    focus:outline-none focus:bg-white focus:border-[#2B72D6] focus:ring-2 focus:ring-[#2B72D6]/20">

                                <option value="">Semua</option>
                                @foreach ($angkatanList as $tahun)
                                    <option value="{{ $tahun }}"
                                        @selected((string) $tahun === (string) $selectedAngkatan)>
                                        {{ $tahun }}
                                    </option>
                                @endforeach
                            </select>

                            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-600">
                                <svg class="h-4 w-4" fill="none" stroke="currentColor"
                                    stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <!-- Filter Bidang Pekerjaan -->
                    <div class="mb-4">
                        <label for="bidang_id"
                            class="block text-sm font-medium text-gray-600 mb-2">
                            Pilih Bidang Pekerjaan
                        </label>

                        <div class="relative">
                            <select name="bidang_id" id="bidang_id" onchange="this.form.submit()"
                                class="appearance-none w-full bg-gray-100 text-[#0F294A] px-4 py-2.5 pr-12 rounded-lg border border-transparent cursor-pointer transition
                                    hover:bg-gray-200/70
                                    focus:outline-none focus:bg-white focus:border-[#2B72D6] focus:ring-2 focus:ring-[#2B72D6]/20">

                                <option value="">Semua</option>
                                @foreach ($bidangList as $b)
                                    <option value="{{ $b['bidang_id'] }}"
                                        @selected((string) $b['bidang_id'] === (string) $selectedBidangId)>
                                        {{ $b['nama_bidang'] }}
                                    </option>
                                @endforeach
                            </select>

                            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-600">
                                <svg class="h-4 w-4" fill="none" stroke="currentColor"
                                    stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>

        <!-- KPI Summary -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6 mb-10 justify-items-center">

            <!-- Total Responden -->
            <div>
                <p class="text-sm text-gray-500 mb-3">
                    Total Responden
                </p>

                <h2 class="text-3xl font-semibold text-[#0F294A]">
                    {{ number_format($totalResponden) }}
                </h2>
            </div>

            <!-- Rata-rata Waktu Tunggu -->
            <div>
                <p class="text-sm text-gray-500 mb-3">
                    Rata-rata Waktu Tunggu
                </p>

                <h2 class="text-3xl font-semibold text-[#0F294A]">
                    {{ number_format($rataWaktu, 2) }}
                    <span class="text-base font-normal ml-1">bln</span>
                </h2>
            </div>

            <!-- Sesuai -->
            <div>
                <p class="text-sm text-gray-500 mb-3">
                    Sesuai
                </p>

                <h2 class="text-3xl font-semibold text-[#2E9E6B]">
                    {{ number_format($persenSesuai, 1) }}%
                </h2>
            </div>

            <!-- Sebagian Sesuai -->
            <div>
                <p class="text-sm text-gray-500 mb-3">
                    Sebagian Sesuai
                </p>

                <h2 class="text-3xl font-semibold text-[#F59E0B]">
                    {{ number_format($persenSebagian, 1) }}%
                </h2>
            </div>

            <!-- Tidak Sesuai -->
            <div>
                <p class="text-sm text-gray-500 mb-3">
                    Tidak Sesuai
                </p>

                <h2 class="text-3xl font-semibold text-[#e73841]">
                    {{ number_format($persenTidak, 1) }}%
                </h2>
            </div>
        </div>

        <hr class="border-gray-200 mb-12">


        <!-- Grafik Distribusi Bidang Pekerjaan dan waktu tunggu -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
            <!-- Distribusi Bidang Pekerjaan -->
            <div class="border border-gray-200 min-w-0 p-4 rounded-xl">
                <h3 class="text-[#0F294A] text-lg font-semibold mb-6">
                    Distribusi Bidang Pekerjaan</h3>

                <div class="relative w-full h-[360px]">
                    <canvas id="bidangChart"></canvas>
                </div>
            </div>

            <!-- Distribusi Waktu Tunggu -->
            <div class="border border-gray-200 min-w-0 p-4 rounded-xl">
                <h3 class="text-[#0F294A] text-lg font-semibold mb-6">
                    Distribusi Waktu Tunggu Kerja
                </h3>

                <div class="relative w-full h-[360px]">
                    <canvas id="waktuChart"></canvas>
                </div>
            </div>
        </div>


        <!-- Kesesuaian Kerja dengan Prodi -->
        <!-- chart kesesuaian pekejaan dengan prodi -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-10">
            <h3 class="text-[#0F294A] text-lg font-semibold mb-6">
                Distribusi Kesesuaian Kerja Dengan Program Studi</h3>

            <div class="relative w-full min-w-0 h-[400px]">
                <canvas id="kesesuaianChart"></canvas>
            </div>
        </div>

        <hr class="border-gray-200 mb-12">

        <!-- Tabel Kesesuaian Pekerjaan dengan Prodi -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Kesesuaian Pekerjaan Dengan Prodi</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Tabel daftar kesesuaian pekerjaan dengan prodi</p>

            <!-- Tabel -->
            <div class="mb-2 overflow-x-auto rounded-lg border border-gray-200">
                <table class="min-w-full text-sm">
                    <thead class="bg-[#1E3A8A] text-left text-white">
                        <tr>
                            <th class="px-4 py-3">Program Studi</th>
                            <th class="px-4 py-3 text-center">Sesuai</th>
                            <th class="px-4 py-3 text-center">Sebagian Sesuai</th>
                            <th class="px-4 py-3 text-center">Tidak Sesuai</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-gray-200">
                        @forelse ($kesesuaianProdi as $row)
                            <tr class="hover:bg-[#2B72D6]/5 transition">
                                <td class="px-4 py-3 font-medium text-[#0F294A]">
                                    {{ $row['prodi'] }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['sesuai'] ?? 0 }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['sebagian sesuai'] ?? 0 }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['tidak sesuai'] ?? 0 }}
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="4"
                                    class="px-4 py-6 text-center text-gray-500">
                                    Belum ada data kesesuaian program studi.
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>  


        <!-- JS -->
        <!-- Chart -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <script>
            const bidangLabels = @json($bidangLabels);
            const bidangJumlah = @json($bidangJumlah);

            const waktuLabels = @json($waktuLabels);
            const waktuJumlah = @json($waktuJumlah);

            const prodiLabels = @json($prodiLabels);
            const sesuaiData = @json($sesuaiData);
            const sebagianData = @json($sebagianData);
            const tidakData = @json($tidakData);

            // 1. Distribusi Bidang Pekerjaan
            new Chart(document.getElementById('bidangChart'), {
                type: 'bar',
                data: {
                    labels: bidangLabels,
                    datasets: [{
                        label: 'Jumlah Responden',
                        data: bidangJumlah,
                        backgroundColor: '#2B72D6',
                        hoverBackgroundColor: '#1E3A8A',
                        borderRadius: 5,
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            },
                            title: {
                                display: true,
                                text: 'Jumlah Responden'
                            }
                        }
                    }
                }
            });

            // 2. Distribusi Waktu Tunggu
            new Chart(document.getElementById('waktuChart'), {
                type: 'bar',
                data: {
                    labels: waktuLabels,
                    datasets: [{
                        label: 'Jumlah Responden',
                        data: waktuJumlah,
                        backgroundColor: '#2B72D6',
                        hoverBackgroundColor: '#1E3A8A',
                        borderRadius: 5,
                        barThickness: 45,
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            },
                            title: {
                                display: true,
                                text: 'Jumlah Responden'
                            }
                        }
                    }
                }
            });

            // 3. Kesesuaian Kerja vs Program Studi
            new Chart(document.getElementById('kesesuaianChart'), {
                type: 'bar',
                data: {
                    labels: prodiLabels,
                    datasets: [
                        {
                            label: 'Sesuai',
                            data: sesuaiData,
                            backgroundColor: '#2B72D6',
                        },
                        {
                            label: 'Sebagian Sesuai',
                            data: sebagianData,
                            backgroundColor: '#F59E0B',
                        },
                        {
                            label: 'Tidak Sesuai',
                            data: tidakData,
                            backgroundColor: '#e73841',
                        }
                    ]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom'
                        }
                    },
                    scales: {

                        x: {
                            stacked: true,
                        },

                        y: {
                            stacked: true,
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            },
                            title: {
                                display: true,
                                text: 'Jumlah Responden'
                            }
                        }
                    }
                }
            });
        </script>

    @endif

@endsection