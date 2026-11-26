@extends('base.fitur1')

@section('hardskill-content')
    <!-- kondisi kondisi -->
    @if ($error)
        <p class="text-red-500">{{ $error }}</p>
    @elseif (!$adaData)
        <p class="text-gray-500">Belum ada data. Silakan upload Excel terlebih dahulu.</p>
    @else
        <!-- tampilan chart -->
        @php
            $batas  = 15;                                           
            $grafik = collect($data)->take($batas);
                   
        @endphp

        <!-- grafik -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-12">
            <h3 class="text-[#0F294A] text-lg font-semibold">Hard Skills yang Dibutuhkan Dunia Kerja</h3>
            @if (count($data) > $batas)
                <p class="mt-2 mb-6 text-sm text-gray-500">
                    Grafik menampilkan {{ $batas }} hard skills teratas dari {{ count($data) }} data. Daftar lengkap ada di tabel
                </p>
            @else
                <p class="mt-2 mb-6 text-sm text-gray-500">
                    Grafik menampilkan {{ count ($data) }} data hard skills yang dibutuhkan dunia kerja
                </p>
            @endif

            <div class="relative w-full min-w-0 h-[424px]">
                <canvas id="chart"></canvas>
            </div>
        </div>

        <!-- <hr class="border-gray-200 mb-10"> -->

        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
        <script>
            const MAX_LABEL = 16;      // batas karakter label sumbu Y
            const Y_AXIS_WIDTH = 112;  // lebar tetap area label (px)

            const semuaLabel = @json($grafik->pluck('skill')->values());

            new Chart(document.getElementById('chart'), {
                type: 'bar',
                data: {
                    labels: semuaLabel,
                    datasets: [{
                        label: 'Jumlah',
                        data: @json($grafik->pluck('jumlah')->values()),
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
                                title: (items) => semuaLabel[items[0].dataIndex]
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
        <!-- tampilan Tabel -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Hard Skills yang Dibutuhkan Dunia Kerja</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Tabel daftar hard skills yang dibutuhkan dunia kerja</p>

            <div class="mb-2 overflow-x-auto rounded-lg border border-gray-200">
                <table class="min-w-full text-sm">
                    <thead class="bg-[#1E3A8A] text-left text-white text-md">
                        <tr>
                            <th class="px-4 py-3 w-24 text-center">No</th>
                            <th class="px-4 py-3">Hard Skill</th>
                            <th class="px-4 py-3 w-48 text-center">Jumlah</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        @forelse ($data as $i => $row)
                            <tr class="hover:bg-[#2B72D6]/5 transition">
                                <td class="px-4 py-3 text-center text-gray-600">{{ $i + 1 }}</td>
                                <td class="px-4 py-3 font-medium text-[#0F294A]">{{ $row['skill'] }}</td>
                                <td class="px-4 py-3 text-center">{{ $row['jumlah'] }}</td>
                            </tr>
                        @empty
                            <tr>
                                <td colspan="3" class="px-4 py-6 text-center text-gray-500">
                                    Belum ada skill untuk bidang ini.
                                </td>
                            </tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>

    @endif
@endsection