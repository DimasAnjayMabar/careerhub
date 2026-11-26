@extends('base.fitur2')

@section('skillgap-content')

    @if ($error)
        <div class="text-red-500 text-center">
            {{ $error }}
        </div>

    @elseif (!$adaDataGap || empty($ranking))
        <div class="text-center text-gray-500">
            Belum ada data skill gap.
        </div>

    @else

        @php
            $batas  = 15;
            $grafik = collect($ranking)->take($batas);

            $skillgap = $grafik->pluck('skill')->values();
            $jumlah   = $grafik->pluck('jumlah')->values();
        @endphp

        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-12">
            <h3 class="text-[#0F294A] text-lg font-semibold">Skill Gap Terbesar</h3>

            <!-- catatan -->
            @if ($catatan)
                <p class="mt-2 mb-6 text-sm text-gray-500">
                    {{ $catatan }}
                </p>
            @endif

            <div class="relative w-full min-w-0 h-[424px]">
                <canvas id="skillGapChart"></canvas>
            </div>

        </div>

        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
        <script>
            const MAX_LABEL = 16;      // batas karakter label sumbu Y
            const Y_AXIS_WIDTH = 112;  // lebar tetap area label (px)

            const skillgap = @json($skillgap);
            const jumlah   = @json($jumlah);

            new Chart(document.getElementById('skillGapChart'), {
                type: 'bar',
                data: {
                    labels: skillgap,
                    datasets: [{
                        label: 'Jumlah Alumni yang Tidak Menyebut Skill',
                        data: jumlah,
                        backgroundColor: '#2B72D6',
                        hoverBackgroundColor: '#1E3A8A',
                        borderRadius: 6,
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                // tooltip menampilkan teks lengkap
                                title: (items) => skillgap[items[0].dataIndex]
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
        <!-- Tabel -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Skill Gap Terbesar</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Tabel daftar skill gap yang ada</p>

            <div class="mb-2 overflow-x-auto rounded-lg border border-gray-200">
                <table class="min-w-full text-sm">
                    <thead class="bg-[#1E3A8A] text-left text-white text-md">
                        <tr>
                            <th class="px-4 py-3 w-24 text-center">No</th>
                            <th class="px-4 py-3">Skill</th>
                            <th class="px-4 py-3 w-48 text-center">Jumlah</th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-gray-200">
                        @forelse ($ranking as $i => $row)
                            <tr class="hover:bg-[#2B72D6]/5 transition">
                                <td class="px-4 py-3 text-center text-gray-600">
                                    {{ $i + 1 }}
                                </td>

                                <td class="px-4 py-3 font-medium text-[#0F294A]">
                                    {{ $row['skill'] }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['jumlah'] }}
                                </td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="3" class="px-4 py-6 text-center text-gray-500">
                                    Belum ada data skill gap.
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </div>


    @endif

@endsection