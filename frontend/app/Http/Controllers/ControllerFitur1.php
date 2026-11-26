<?php

namespace App\Http\Controllers;

use App\Services\SkillApi;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Request;

class ControllerFitur1 extends Controller
{
    public function hardSkills(Request $request, SkillApi $api)
    {
        return $this->tampilPerBidang('hard', 'main.fitur1_hardskill', $request, $api);
    }

    public function softSkills(Request $request, SkillApi $api)
    {
        return $this->tampilPerBidang('soft', 'main.fitur1_softskill', $request, $api);
    }

    public function sertifikasi(Request $request, SkillApi $api)
    {
        return $this->tampilPerBidang('sert', 'main.fitur1_sertifikasi', $request, $api);
    }

    public function matriks(SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        return view('main.fitur1_matrix', [
            'error'      => $error,
            'adaData'    => $payload['meta']['ada_data'] ?? false,
            'matrix'     => $payload['matrix'] ?? [],
            'bidangList' => $this->semuaBidang($payload),
        ]);
    }

    private function ambil(SkillApi $api): array
    {
        try {
            return [$api->feature1(), null];
        } catch (ConnectionException $e) {
            return [[], 'Backend Python belum berjalan.'];
        } catch (RequestException $e) {
            return [[], 'Backend Python mengembalikan error.'];
        }
    }

    // semua bidang filter
    private function semuaBidang(array $payload): array
    {
        $list = array_unique(array_merge(
            array_keys($payload['hard'] ?? []),
            array_keys($payload['soft'] ?? []),
            array_keys($payload['sert'] ?? []),
        ));

        sort($list, SORT_NATURAL | SORT_FLAG_CASE);

        return array_values($list);
    }

    
    private function gabungkan(array $perBidang): array
    {
        $total = [];

        foreach ($perBidang as $rows) {
            foreach ($rows as $row) {
                // kunci nama: 'skill', atau 'sertifikasi', atau kunci pertama selain 'jumlah'
                $kunciNama = isset($row['skill']) ? 'skill'
                    : (isset($row['sertifikasi']) ? 'sertifikasi'
                    : array_key_first(array_diff_key($row, ['jumlah' => 1])));

                if ($kunciNama === null) {
                    continue;
                }

                $nama = $row[$kunciNama];
                $total[$nama] ??= [$kunciNama => $nama, 'jumlah' => 0];
                $total[$nama]['jumlah'] += (int) ($row['jumlah'] ?? 0);
            }
        }

        $hasil = array_values($total);
        usort($hasil, fn ($a, $b) => $b['jumlah'] <=> $a['jumlah']);

        return $hasil;
    }

    private function tampilPerBidang(string $kunci, string $view, Request $request, SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        // PERBAIKAN: sebelumnya array_keys($payload[$kunci]) -> hanya bidang yang punya data kategori ini
        $bidangList = $this->semuaBidang($payload);

        // Pilihan "Semua Bidang" mengirim ?bidang= (kosong). Parameter tidak ada atau tidak valid
        // juga dianggap Semua Bidang, jadi $bidang = null berarti tampilkan semua.
        $bidang = $request->query('bidang');
        if (!in_array($bidang, $bidangList, true)) {
            $bidang = null;
        }
        $semua = $bidang === null;

        return view($view, [
            'error'      => $error,
            'adaData'    => $payload['meta']['ada_data'] ?? false,
            'bidangList' => $bidangList,
            'bidang'     => $bidang,
            'semua'      => $semua,
            // satu bidang: data bidang itu. Semua bidang: jumlah tiap skill dijumlahkan lintas bidang,
            // bentuknya sama dengan data satu bidang, jadi view grafik dan tabel tidak perlu diubah.
            'data'       => $semua
                ? $this->gabungkan($payload[$kunci] ?? [])
                : ($payload[$kunci][$bidang] ?? []),
        ]);
    }
}