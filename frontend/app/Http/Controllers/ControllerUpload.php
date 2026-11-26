<?php

namespace App\Http\Controllers;

use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Http\UploadedFile;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;

class ControllerUpload extends Controller
{
    private const PREVIEW_LIMIT = 8;
    private const PER_PAGE = 10;
    private const CACHE_KEY = 'master_data.current_file';

    // =====================================================
    // HALAMAN MASTER DATA
    // =====================================================

    public function index(Request $request)
    {
        $file = $this->getCurrentFile();
        $showAll = $request->query('tampil') === 'semua';

        $rows = [];
        $total = 0;
        $paginator = null;

        if ($file) {
            $page = max(1, (int) $request->query('page', 1));

            $perPage = $showAll
                ? self::PER_PAGE
                : self::PREVIEW_LIMIT;

            $result = $this->getRows(
                $showAll ? $page : 1,
                $perPage
            );

            $rows = $result['data'];
            $total = $result['total'];

            if ($showAll) {
                $paginator = new LengthAwarePaginator(
                    $rows,
                    $total,
                    self::PER_PAGE,
                    $page,
                    [
                        'path' => $request->url(),
                        'query' => ['tampil' => 'semua'],
                    ]
                );
            }
        }

        return view('base.upload', [
            'file' => $file,
            'rows' => $rows,
            'total' => $total,
            'showAll' => $showAll,
            'paginator' => $paginator,
            'previewLimit' => self::PREVIEW_LIMIT,
        ]);
    }

    // =====================================================
    // UPLOAD FILE EXCEL
    // =====================================================

    public function upload(Request $request): RedirectResponse
    {
        $request->validate(
            [
                'file' => [
                    'required',
                    'file',
                    'mimes:xlsx,xls',
                    'max:10240',
                ],
            ],
            [
                'file.required' => 'Pilih file Excel terlebih dahulu.',
                'file.mimes' => 'Format file harus .xlsx atau .xls.',
                'file.max' => 'Ukuran file maksimal 10 MB.',
                'file.uploaded' => 'File gagal diunggah. Coba lagi.',
            ]
        );

        $uploaded = $request->file('file');

        try {
            $summary = $this->sendToBackend($uploaded);

        } catch (ConnectionException $e) {
            report($e);

            return back()->withErrors([
                'file' => 'Tidak bisa terhubung ke server data. Coba lagi beberapa saat.',
            ]);

        } catch (\Throwable $e) {
            report($e);

            return back()->withErrors([
                'file' => $e->getMessage(),
            ]);
        }

        // Simpan informasi file aktif
        Cache::forever(self::CACHE_KEY, [
            'filename' => $uploaded->getClientOriginalName(),
            'uploaded_at' => now()->toDateTimeString(),
            'total_rows' => $summary['jumlah_diproses'] ?? 0,
        ]);

        return redirect()
            ->route('base.upload.index')
            ->with('success', 'File berhasil diunggah dan menggantikan data sebelumnya.')
            ->with('upload_summary', $summary);
    }

    // =====================================================
    // HAPUS DATA
    // =====================================================

    public function destroy(): RedirectResponse
    {
        try {
            Http::timeout(30)
                ->delete($this->backendUrl('responden'))
                ->throw();

        } catch (ConnectionException $e) {
            report($e);

            return back()->withErrors([
                'file' => 'Tidak bisa terhubung ke server data.',
            ]);

        } catch (\Throwable $e) {
            report($e);

            return back()->withErrors([
                'file' => 'Gagal menghapus data responden.',
            ]);
        }

        // Hapus informasi file aktif
        Cache::forget(self::CACHE_KEY);

        return redirect()
            ->route('base.upload.index')
            ->with('success', 'Data berhasil dihapus.');
    }

    // =====================================================
    // AMBIL INFORMASI FILE AKTIF
    // =====================================================

    private function getCurrentFile(): ?array
    {
        return Cache::get(self::CACHE_KEY);
    }

    // =====================================================
    // AMBIL DATA RESPONDEN
    // =====================================================

    /**
     * @return array{data: array<int, array>, total: int}
     */
    private function getRows(int $page, int $perPage): array
    {
        $response = Http::timeout(30)
            ->get($this->backendUrl('responden'), [
                'page' => $page,
                'limit' => $perPage,
            ])
            ->throw()
            ->json();

        return [
            'data' => $response['data'] ?? [],
            'total' => $response['total'] ?? 0,
        ];
    }

    // =====================================================
    // KIRIM FILE KE FASTAPI
    // =====================================================

    private function sendToBackend(UploadedFile $file): array
    {
        $response = Http::timeout(120)
            ->attach(
                'file',
                file_get_contents($file->getRealPath()),
                $file->getClientOriginalName()
            )
            ->post($this->backendUrl('ingest'));

        if ($response->failed()) {
            $detail = $response->json('detail');

            throw new \RuntimeException(
                is_string($detail)
                    ? $detail
                    : 'Server menolak file. Periksa isi dan format kolomnya.'
            );
        }

        $data = $response->json();

        if (!($data['ok'] ?? false)) {
            throw new \RuntimeException(
                $data['error'] ?? 'Gagal memproses file Excel.'
            );
        }

        return $data['summary'] ?? $data;
    }

    // =====================================================
    // HELPER URL FASTAPI
    // =====================================================

    private function backendUrl(string $endpoint): string
    {
        return rtrim(
            (string) config('services.career_api.url'),
            '/'
        ) . '/' . ltrim($endpoint, '/');
    }
}
