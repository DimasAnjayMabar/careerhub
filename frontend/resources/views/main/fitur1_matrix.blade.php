@extends('base.fitur1')

@section('matrix-content')
    @if (!empty($error))
        <p class="text-red-500">{{ $error }}</p>
    @elseif (empty($adaData) || empty($matrix))
        <p class="text-gray-500">Belum ada data. Silakan upload Excel terlebih dahulu.</p>
    @else
        @php
            $prodiList = array_keys($matrix);

            // satu baris per bidang, buang bidang yang tidak punya alumni, urutkan dari terbanyak
            $baris = collect($bidangList)
                ->map(function ($b) use ($matrix, $prodiList) {
                    $sel = [];
                    foreach ($prodiList as $p) {
                        $sel[$p] = $matrix[$p][$b] ?? 0;
                    }
                    return ['bidang' => $b, 'sel' => $sel, 'total' => array_sum($sel)];
                })
                ->filter(fn ($r) => $r['total'] > 0)
                ->sortByDesc('total')
                ->values();

            $totalKolom = [];
            foreach ($prodiList as $p) {
                $totalKolom[$p] = $baris->sum(fn ($r) => $r['sel'][$p]);
            }
        @endphp

        <!-- Informasi -->
        <p class="text-sm font-medium text-gray-800">
            Informasi</p>
        <div class="flex mt-2 gap-10">
            <p class="text-xs text-gray-600">
                Baris = Bidang pekerjaan</p>
            <span class="text-xs text-gray-600">
                Kolom = Prodi</span>
        </div>
        <p class="mt-2 text-xs text-gray-600 mb-10">
            Angka = Jumlah alumni dari prodi tersebut yang bekerja di bidang itu</p>

        <!-- tabel -->
        <div class="overflow-x-auto rounded-lg border border-gray-200 mb-8">
            <table class="min-w-full text-sm">
                <thead class="bg-[#1E3A8A] text-white">
                    <tr>
                        <th class="px-4 py-3 text-left font-semibold sticky left-0 z-10 bg-[#1E3A8A]">Bidang Pekerjaan</th>
                        @foreach ($prodiList as $p)
                            <th class="px-4 py-3 text-center font-semibold whitespace-nowrap">{{ $p }}</th>
                        @endforeach
                        <th class="px-4 py-3 text-center font-semibold sticky right-0 z-10 bg-[#162d6b] border-l border-white/20">Total</th>
                    </tr>
                </thead>

                <tbody class="divide-y divide-gray-100">
                    @foreach ($baris as $r)
                        <tr class="hover:bg-[#2B72D6]/5 transition">
                            <td class="px-4 py-3 font-medium text-[#0F294A] sticky left-0 z-10 bg-white whitespace-nowrap">
                                {{ $r['bidang'] }}
                            </td>

                            @foreach ($prodiList as $p)
                                @php $v = $r['sel'][$p]; @endphp
                                @if ($v > 0)
                                    <td class="px-4 py-3 text-center font-semibold bg-[#2B72D6]/10 text-[#1E3A8A]">{{ $v }}</td>
                                @else
                                    <td class="px-4 py-3 text-center text-gray-300">–</td>
                                @endif
                            @endforeach

                            <td class="px-4 py-3 text-center font-bold text-[#1E3A8A] sticky right-0 z-10 bg-gray-50 border-l border-gray-200">
                                {{ $r['total'] }}
                            </td>
                        </tr>
                    @endforeach
                </tbody>

                <tfoot class="bg-gray-100 font-bold text-[#0F294A]">
                    <tr>
                        <td class="px-4 py-3 sticky left-0 z-10 bg-gray-100">Total</td>
                        @foreach ($prodiList as $p)
                            <td class="px-4 py-3 text-center">{{ $totalKolom[$p] }}</td>
                        @endforeach
                        <td class="px-4 py-3 text-center text-[#1E3A8A] sticky right-0 z-10 bg-gray-100 border-l border-gray-200">
                            {{ array_sum($totalKolom) }}
                        </td>
                    </tr>
                </tfoot>
            </table>
        </div>

    @endif
@endsection