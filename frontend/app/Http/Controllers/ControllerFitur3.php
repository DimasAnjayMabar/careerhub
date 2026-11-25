<?php

namespace App\Http\Controllers;

use App\Services\SkillApi;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Request;

class ControllerFitur3 extends Controller
{
    public function dashboard(Request $request, SkillApi $api)
    {
        // Mengambil filter yang dipilih pengguna
        $validated = $request->validate([
            'angkatan' => ['nullable', 'integer'],
            'bidang_id' => ['nullable', 'integer'],
        ]);

        $angkatan = isset($validated['angkatan'])
            ? (int) $validated['angkatan']
            : null;

        $bidangId = isset($validated['bidang_id'])
            ? (int) $validated['bidang_id']
            : null;

        // Mengambil pilihan dropdown filter
        [$filters, $error] = $this->ambilFilter($api);

        // Mengambil data dashboard berdasarkan filter
        if (!$error) {
            [$payload, $error] = $this->ambilDashboard(
                $api,
                $angkatan,
                $bidangId
            );
        } else {
            $payload = [];
        }

        return view('main.fitur3_dashboard', [
            'error'             => $error,

            // Data filter
            'angkatanList'      => $filters['angkatan'] ?? [],
            'bidangList'        => $filters['bidang'] ?? [],

            // Filter yang sedang dipilih
            'selectedAngkatan'  => $angkatan,
            'selectedBidangId'  => $bidangId,

            // KPI
            'kpi'               => $payload['kpi'] ?? [],

            // Data diagram
            'distribusiBidang'  => $payload['distribusi_bidang'] ?? [],
            'distribusiWaktu'   => $payload['distribusi_waktu'] ?? [],

            // Data tabel dan diagram kesesuaian
            'kesesuaianProdi'   => $payload['kesesuaian_prodi'] ?? [],
        ]);
    }

    // Mengambil pilihan filter dari backend
    private function ambilFilter(SkillApi $api): array
    {
        try {
            return [$api->feature3Filters(), null];

        } catch (ConnectionException $e) {
            return [[], 'Backend Python belum berjalan.'];

        } catch (RequestException $e) {
            return [[], 'Backend Python mengembalikan error.'];
        }
    }

    // Mengambil data dashboard sesuai filter
    private function ambilDashboard(
        SkillApi $api,
        ?int $angkatan,
        ?int $bidangId
    ): array {
        try {
            return [
                $api->feature3($angkatan, $bidangId),
                null
            ];

        } catch (ConnectionException $e) {
            return [[], 'Backend Python belum berjalan.'];

        } catch (RequestException $e) {
            return [[], 'Backend Python mengembalikan error.'];
        }
    }
}