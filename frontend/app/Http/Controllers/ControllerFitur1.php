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
        return $this->tampilPerBidang('hard', 'main.hardskill_fitur1', $request, $api);
    }

    public function softSkills(Request $request, SkillApi $api)
    {
        return $this->tampilPerBidang('soft', 'main.softskill_fitur1', $request, $api);
    }

    public function sertifikasi(Request $request, SkillApi $api)
    {
        return $this->tampilPerBidang('sert', 'main.sertifikasi_fitur1', $request, $api);
    }

    public function matriks(SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        return view('main.matrix_fitur1', [
            'error'      => $error,
            'adaData'    => $payload['meta']['ada_data'] ?? false,
            'matrix'     => $payload['matrix'] ?? [],
            'bidangList' => array_keys($payload['hard'] ?? []),
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

    private function tampilPerBidang(string $kunci, string $view, Request $request, SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        $bidangList = array_keys($payload[$kunci] ?? []);
        $bidang     = $request->query('bidang', $bidangList[0] ?? null);

        return view($view, [
            'error'      => $error,
            'adaData'    => $payload['meta']['ada_data'] ?? false,
            'bidangList' => $bidangList,
            'bidang'     => $bidang,
            'data'       => $payload[$kunci][$bidang] ?? [],
        ]);
    }
}