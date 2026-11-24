<?php

namespace App\Http\Controllers;

use App\Services\SkillApi;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;

class ControllerFitur2 extends Controller
{
    // 1. Skill Gap
    public function skillGap(SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        return view('main.fitur2_skillgap', [
            'error'      => $error,
            'adaData'    => $payload['meta']['ada_data'] ?? false,
            'adaDataGap' => $payload['meta']['ada_data_gap'] ?? false,
            'catatan'    => $payload['meta']['catatan'] ?? null,
            'ranking'    => $payload['ranking_gap'] ?? [],
        ]);
    }

    // 2. Dibutuhkan vs Tidak Disebut
    public function dibutuhkanVsTidakDisebut(SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        return view('main.fitur2_dibutuhkan', [
            'error'    => $error,
            'adaData'  => $payload['meta']['ada_data'] ?? false,
            'catatan'  => $payload['meta']['catatan'] ?? null,
            'banding'  => $payload['dibutuhkan_vs_kurang'] ?? [],
        ]);
    }

    // 3. Tren Antar Angkatan
    public function tren(SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        $data = $this->olahTren($payload);

        return view('main.fitur2_tren', array_merge([
            'error'   => $error,
            'adaData' => $payload['meta']['ada_data'] ?? false,
            'catatan' => $payload['meta']['catatan'] ?? null,
        ], $data));
    }

    // 4. Waktu Tunggu
    public function waktuTunggu(SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        $data = $this->olahWaktuTunggu($payload);

        return view('main.fitur2_waktu_tunggu', array_merge([
            'error'   => $error,
            'adaData' => $payload['meta']['ada_data'] ?? false,
            'catatan' => $payload['meta']['catatan'] ?? null,
        ], $data));
    }

    // Mengambil data dari backend Python
    private function ambil(SkillApi $api): array
    {
        try {
            return [$api->feature2(), null];
        } catch (ConnectionException $e) {
            return [[], 'Backend Python belum berjalan.'];
        } catch (RequestException $e) {
            return [[], 'Backend Python mengembalikan error.'];
        }
    }

    // Mengolah data tren antar angkatan
    private function olahTren(array $payload): array
    {
        $tren = $payload['tren_antar_angkatan'] ?? [];

        ksort($tren);

        $angkatan = array_map('strval', array_keys($tren));

        $total = [];
        $dataPerAngkatan = [];

        foreach ($tren as $rows) {
            $perSkill = [];

            foreach ($rows as $r) {
                $skill = $r['skill'] ?? null;
                $jumlah = $r['jumlah'] ?? 0;

                if (!$skill) {
                    continue;
                }

                $total[$skill] = ($total[$skill] ?? 0) + $jumlah;
                $perSkill[$skill] = $jumlah;
            }

            $dataPerAngkatan[] = $perSkill;
        }

        // Mengurutkan skill berdasarkan total jumlah
        arsort($total);

        // Mengambil 5 skill teratas
        $trenSeries = [];

        foreach (array_slice(array_keys($total), 0, 5) as $skill) {
            $vals = [];

            foreach ($dataPerAngkatan as $rows) {
                $vals[] = $rows[$skill] ?? 0;
            }

            $trenSeries[] = [
                'skill' => $skill,
                'data'  => $vals,
            ];
        }

        return [
            'angkatan'   => $angkatan,
            'trenSeries' => $trenSeries,
        ];
    }

   // Mengolah rata-rata waktu tunggu per angkatan
    private function olahWaktuTunggu(array $payload): array
    {
    $rows = $payload['waktu_tunggu_vs_gap'] ?? [];

    $kelompok = [];

    foreach ($rows as $r) {
        if (!isset($r['angkatan'], $r['waktu_bulan'])) {
            continue;
        }

        $angkatan = (int) $r['angkatan'];
        $waktu = (float) $r['waktu_bulan'];

        $kelompok[$angkatan][] = $waktu;
    }

    ksort($kelompok);

    $angkatanLabels = [];
    $rataWaktu = [];
    $jumlahResponden = [];

    foreach ($kelompok as $angkatan => $waktu) {
        $angkatanLabels[] = (string) $angkatan;

        $rataWaktu[] = round(
            array_sum($waktu) / count($waktu),
            2
        );

        $jumlahResponden[] = count($waktu);
    }

    return [
        'angkatanLabels'  => $angkatanLabels,
        'rataWaktu'       => $rataWaktu,
        'jumlahResponden' => $jumlahResponden,
    ];
}
}