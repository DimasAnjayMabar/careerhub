@extends('base.fitur2')

@section('tren-angkatan-content')

    @if ($error)
        <div class="text-red-500 text-center">
            {{ $error }}
        </div>

    @elseif (empty($angkatan) || empty($trenSeries))
        <div class="text-center text-gray-500">
            Belum ada data tren skill gap antar angkatan.
        </div>

    @else

        @php
            $labelAngkatan = $angkatan;
        @endphp

        <!-- Analisis Chart -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-12">
            <h3 class="text-[#0F294A] text-lg font-semibold">Tren Skill Tidak Disebut per Angkatan</h3>

            <!-- Catatan -->
            @if ($catatan)
                <p class="mt-2 mb-6 text-sm text-gray-500">
                    5 skill dominan yang paling sering tidak disebut alumni
                </p>
            @endif

            <div class="relative w-full min-w-0 h-[420px] mt-8">
                <canvas id="trenChart"></canvas>
            </div>

        </div>

        <!-- Chart.js -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <script>
            const angkatan = @json($labelAngkatan);
            const trenSeries = @json($trenSeries);

            const warna = [
                '#2B72D6',
                '#93C5FD',
                '#0F294A',
                '#F59E0B',
                '#10B981'
            ];

            const datasets = trenSeries.map((item, index) => ({
                label: item.skill,
                data: item.data,
                borderColor: warna[index % warna.length],
                backgroundColor: warna[index % warna.length],
                borderWidth: 2.5,
                tension: 0,          // garis lurus antar titik
                fill: false,
                pointRadius: 4,
                pointHoverRadius: 6
            }));

            new Chart(document.getElementById('trenChart'), {
                type: 'line',

                data: {
                    labels: angkatan,
                    datasets: datasets
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            align: 'end'
                        }
                    },

                    scales: {
                        x: {
                            title: { display: true, text: 'Angkatan' }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0 },
                            title: { display: true, text: 'Jumlah Responden' }
                        }
                    }
                }
                });
        </script>

       <!-- tabel -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Tren Skill Tidak Disebut per Angkatan</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Tabel daftar tren skill antar angkatan</p>

            <!-- Tabel -->
            <div class="mt-6 overflow-x-auto rounded-lg border border-gray-200">

                <table class="min-w-full text-sm">

                    <thead class="bg-[#1E3A8A] text-white">
                        <tr>
                            <th class="px-4 py-3 text-center">No</th>
                            <th class="px-4 py-3">Skill</th>

                            @foreach ($angkatan as $tahun)
                                <th class="px-4 py-3 text-center">
                                    {{ $tahun }}
                                </th>
                            @endforeach
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-gray-200">

                        @foreach ($trenSeries as $i => $row)

                            <tr class="hover:bg-[#2B72D6]/5 transition">

                                <td class="px-4 py-3 text-center text-gray-600">
                                    {{ $i + 1 }}
                                </td>

                                <td class="px-4 py-3 font-medium text-[#0F294A]">
                                    {{ $row['skill'] }}
                                </td>

                                @foreach ($angkatan as $index => $tahun)
                                    <td class="px-4 py-3 text-center">
                                        {{ $row['data'][$index] ?? 0 }}
                                    </td>
                                @endforeach

                            </tr>

                        @endforeach

                    </tbody>
                </table>
            </div>
        </div>

    @endif

@endsection