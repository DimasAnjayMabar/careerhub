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
        <div class="w-full bg-white border border-gray-200 rounded-xl p-6 mb-6">

            <div class="flex items-center gap-2.5">
                <svg class="w-8 h-8 shrink-0" fill="none" stroke="#0F294A" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round"d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0 0 20.25 18V6A2.25 2.25 0 0 0 18 3.75H6A2.25 2.25 0 0 0 3.75 6v12A2.25 2.25 0 0 0 6 20.25Z" />
                </svg>

                <span class="text-[#0F294A] text-lg font-semibold">
                    Chart Tren Skill Antar Angkatan
                </span>
            </div>

            <!-- Catatan -->
            @if ($catatan)
                <p class="text-sm text-gray-500 mt-4">
                    {{ $catatan }}
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
                tension: 0.3,
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
                            title: {
                                display: true,
                                text: 'Angkatan'
                            }
                        },

                    }
                }
            });
        </script>

       <!-- tabel -->
        <div class="w-full border border-gray-200 p-6 rounded-xl mb-6">
            <div class="flex items-center gap-2.5">

                <svg class="w-8 h-8 shrink-0" fill="none"stroke="#0F294A" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 0 1-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0 1 12 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 1.5v-1.5m0 0c0-.621.504-1.125 1.125-1.125m0 0h7.5" />
                </svg>

                <span class="text-[#0F294A] text-lg font-semibold">
                    Tabel Tren Skill Antar Angkatan
                </span>
            </div>

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