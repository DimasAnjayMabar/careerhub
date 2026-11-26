@extends('base.fitur2')

@section('waktu-tunggu-content')

    @if ($error)
        <div class="text-red-500 text-center">
            {{ $error }}
        </div>

    @elseif (empty($angkatanLabels))
        <div class="text-center text-gray-500">
            Belum ada data waktu tunggu.
        </div>

    @else

        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Rata-Rata Waktu Tunggu Antar Angkatan</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Rata-rata lama menunggu pekerjaan pertama per angkatan</p>

            <!-- Chart -->
            <div class="relative w-full min-w-0 h-[424px]">
                <canvas id="waktuTungguChart"></canvas>
            </div>

        </div>

        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
        <script>
            const angkatan        = @json($angkatanLabels);
            const rataWaktu       = @json($rataWaktu);
            const jumlahResponden = @json($jumlahResponden);

            new Chart(document.getElementById('waktuTungguChart'), {
                type: 'bar',
                data: {
                    labels: angkatan,
                    datasets: [{
                        label: 'Rata-rata Waktu Tunggu',
                        data: rataWaktu,
                        backgroundColor: '#2B72D6',
                        hoverBackgroundColor: '#1E3A8A',
                        borderRadius: 6,
                        maxBarThickness: 45
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (ctx) =>
                                    `Rata-rata ${ctx.parsed.y} bulan (n = ${jumlahResponden[ctx.dataIndex]})`
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: { display: true, text: 'Bulan' }
                        },
                        x: {
                            title: { display: true, text: 'Angkatan' }
                        }
                    }
                }
            });
        </script>

        <!-- Tabel -->
        <div class="w-full bg-white border border-gray-200 rounded-xl p-4 mb-8">
            <h3 class=" text-[#0F294A] text-lg font-medium">Rata-Rata Waktu Tunggu Antar Angkatan</h3>
            <p class="mt-2 mb-6 text-sm text-gray-500">Tabel daftar waktu tunggu antar angkatan</p>
            
            <!-- Tabel -->
            <div class="mb-2 overflow-x-auto rounded-lg border border-gray-200">
                <table class="min-w-full text-sm">

                    <thead class="bg-[#1E3A8A] text-left text-white">
                        <tr>
                            <th class="px-4 py-3 w-24 text-center">No</th>
                            <th class="px-4 py-3">Angkatan</th>
                            <th class="px-4 py-3 text-center">
                                Jumlah Responden
                            </th>
                            <th class="px-4 py-3 text-center">
                                Rata-rata Waktu Tunggu (Bulan)
                            </th>
                        </tr>
                    </thead>

                    <tbody class="divide-y divide-gray-200">
                        @foreach ($angkatanLabels as $i => $tahun)
                            <tr class="hover:bg-[#2B72D6]/5 transition">

                                <td class="px-4 py-3 text-center text-gray-600">
                                    {{ $i + 1 }}
                                </td>

                                <td class="px-4 py-3 font-medium text-[#0F294A]">
                                    {{ $tahun }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $jumlahResponden[$i] }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ number_format($rataWaktu[$i], 2) }}
                                </td>

                            </tr>
                        @endforeach
                    </tbody>

                </table>
            </div>
        </div>

    @endif

@endsection