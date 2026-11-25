<?php

namespace App\Http\Controllers;

use App\Services\SkillApi;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Request;

class ControllerFitur4 extends Controller
{
    // Halaman Career Navigation System
    public function careerNavigation(Request $request, SkillApi $api)
    {
        [$payload, $error] = $this->ambil($api);

        $data = $this->siapkanData($payload, $error, $request);

        if ($request->route('tab') === 'matcher') {

            $hasilMatch = session('career_match_result', []);

            $data = array_merge($data, [
                'hasil'          => $hasilMatch['hasil'] ?? [],
                'matchError'     => $hasilMatch['matchError'] ?? null,
                'insight'        => $hasilMatch['insight'] ?? ($data['insight'] ?? []),
                'meta'           => $hasilMatch['meta'] ?? [],
                'skillDipilih'   => $hasilMatch['skillDipilih'] ?? [],
                'hasMatchResult' => $hasilMatch['hasMatchResult'] ?? false,
            ]);

            return view('main.fitur4_navigasikarir', $data);
        }

    return view('main.fitur4_karirexplore', $data);
    }

    // Menghitung rekomendasi karier
    public function match(Request $request, SkillApi $api)
    {
        $validated = $request->validate([
            'skill_ids'   => ['required', 'array', 'min:1'],
            'skill_ids.*' => ['required', 'integer'],
        ]);

        $hasil = [];
        $matchError = null;

        try {
            $hasil = $api->match(
                array_map('intval', $validated['skill_ids'])
            );

            $matchError = $hasil['error'] ?? null;

        } catch (ConnectionException $e) {
            $matchError = 'Backend Python belum berjalan.';

        } catch (RequestException $e) {
            $matchError = 'Backend Python mengembalikan error.';
        }

        return redirect('/career-navigation/matcher')
            ->with('career_match_result', [
                'hasil'          => $hasil['hasil'] ?? [],
                'matchError'     => $matchError,
                'insight'        => $hasil['insight'] ?? [],
                'meta'           => $hasil['meta'] ?? [],
                'skillDipilih'   => $validated['skill_ids'],
                'hasMatchResult' => true,
            ]);
    }

    // Mengambil data awal Feature 4
    private function ambil(SkillApi $api): array
    {
        try {
            return [$api->feature4(), null];
        } catch (ConnectionException $e) {
            return [[], 'Backend Python belum berjalan.'];
        } catch (RequestException $e) {
            return [[], 'Backend Python mengembalikan error.'];
        }
    }

    // Data yang dikirim ke menu
    private function siapkanData(
        array $payload,
        ?string $error,
        Request $request
    ): array {
        $explorer = $payload['explorer'] ?? [];

        $bidangList = $explorer['bidang'] ?? [];
        $cards = collect($explorer['cards'] ?? []);

        // Bidang pertama
        $bidang1 = $request->query('bidang1');

        // Bidang kedua 
        $bidang2 = $request->query('bidang2');

        // Mengambil kartu berdasarkan bidang yang dipilih
        $card1 = $cards->firstWhere('nama_bidang', $bidang1) ?? [];
        $card2 = $bidang2
            ? ($cards->firstWhere('nama_bidang', $bidang2) ?? [])
            : [];

        return [
            'error'       => $error,

            // Career Explorer
            'bidangList'  => $bidangList,
            'bidang1'     => $bidang1,
            'bidang2'     => $bidang2,
            'card1'       => $card1,
            'card2'       => $card2,

            // Career Matcher
            'hardSkills'  => $payload['skill_options']['hard'] ?? [],
            'softSkills'  => $payload['skill_options']['soft'] ?? [],
            'insight'     => $payload['insight'] ?? [],

            // Hasil rekomendasi
            'hasil'       => [],
            'meta'        => [],
            'matchError'  => null,
            'skillDipilih' => [],

            'activeTab'   => $request->input('tab', 'explorer'),
        ];
    }
}