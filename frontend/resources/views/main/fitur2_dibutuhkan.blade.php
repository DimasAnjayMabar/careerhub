@extends('base.fitur2')

@section('dibutuhkan-content')

    @if ($error)
        <div class="text-red-500 text-center">
            {{ $error }}
        </div>

    @elseif (empty($banding))
        <div class="text-center text-gray-500">
            Belum ada data perbandingan skill.
        </div>

    @else

        @php
            $batas   = 15;
            $grafik  = collect($banding)->take($batas);

            $skill        = $grafik->pluck('skill')->values();
            $dibutuhkan   = $grafik->pluck('dibutuhkan')->values();

            $tidakDisebut = $grafik->pluck('dirasa_kurang')->values();
        @endphp

        <!-- Analisis Chart -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-12">
            <h3 class="text-[#0F294A] text-lg font-semibold">Perbandingan Skill yang Dibutuhkan dan Tidak Disebut</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">
                Perbandingan skill yang dibutuhkan dan tidak disebut oleh alumni
            </p>

            <div class="relative w-full min-w-0 h-[424px] mt-8">
                <canvas id="dibutuhkanChart"></canvas>
            </div>

        </div>

        <!-- Chart.js -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
        <script>
            const MAX_LABEL = 16;      // batas karakter label sumbu Y
            const Y_AXIS_WIDTH = 112;  // lebar tetap area label (px)

            const skill        = @json($skill);
            const dibutuhkan   = @json($dibutuhkan);
            const tidakDisebut = @json($tidakDisebut);

            new Chart(document.getElementById('dibutuhkanChart'), {
                type: 'bar',
                data: {
                    labels: skill,
                    datasets: [
                        {
                            label: 'Dibutuhkan',
                            data: dibutuhkan,
                            backgroundColor: '#2B72D6',
                            hoverBackgroundColor: '#1E3A8A',
                            borderRadius: 6,
                        },
                        {
                            label: 'Tidak Disebut',
                            data: tidakDisebut,
                            backgroundColor: '#F59E0B',
                            hoverBackgroundColor: '#D97706',
                            borderRadius: 6,
                        }
                    ]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            align: 'end'
                        },
                        tooltip: {
                            callbacks: {
                                // tooltip menampilkan teks lengkap
                                title: (items) => skill[items[0].dataIndex]
                            }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: { precision: 0 },
                            title: { display: true, text: 'Jumlah' }
                        },
                        y: {
                            // kunci lebar area label supaya posisi grafik konsisten
                            afterFit: (scale) => { scale.width = Y_AXIS_WIDTH; },
                            ticks: {
                                autoSkip: false,
                                callback: function (value) {
                                    const label = this.getLabelForValue(value);
                                    return label.length > MAX_LABEL
                                        ? label.slice(0, MAX_LABEL - 1) + '…'
                                        : label;
                                }
                            }
                        }
                    }
                }
            });
        </script>

        <!--  -->
        <!--  Tabel -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Perbandingan Skill yang Dibutuhkan dan Tidak Disebut</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Tabel perbandingan skill yang dibutuhkan namun tidak disebut</p>

            <div class="mb-2 overflow-x-auto rounded-lg border border-gray-200">
                <table class="min-w-full text-sm">
                    <thead class="bg-[#1E3A8A] text-left text-white text-md">
                        <tr>
                            <th class="px-4 py-3 w-24 text-center">No</th>
                            <th class="px-4 py-3">Skill</th>
                            <th class="px-4 py-3 text-center">Dibutuhkan</th>
                            <th class="px-4 py-3 text-center">Tidak Disebut</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-gray-200">

                        @forelse ($banding as $i => $row)

                            <tr class="hover:bg-[#2B72D6]/5 transition">

                                <td class="px-4 py-3 text-center text-gray-600">
                                    {{ $i + 1 }}
                                </td>

                                <td class="px-4 py-3 font-medium text-[#0F294A]">
                                    {{ $row['skill'] }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['dibutuhkan'] }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['dirasa_kurang'] }}
                                </td>

                            </tr>

                        @empty

                            <tr>
                                <td colspan="4" class="px-4 py-6 text-center text-gray-500">
                                    Belum ada data perbandingan skill.
                                </td>
                            </tr>

                        @endforelse

                    </tbody>
                </table>
            </div>
        </div>

    @endif

@endsection