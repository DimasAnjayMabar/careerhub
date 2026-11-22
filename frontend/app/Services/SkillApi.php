<?php

namespace App\Services;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Http;

class SkillApi
{
    protected function client()
    {
        return Http::baseUrl(config('services.python.url'))
            ->acceptJson()
            ->timeout(15);
    }

    public function feature1(): array
    {
        return $this->client()->get('/feature1/data')->throw()->json();
    }

    public function feature2(): array
    {
        return $this->client()->get('/feature2/data')->throw()->json();
    }

    public function feature3(?int $angkatan = null, ?int $bidangId = null): array
    {
        return $this->client()
            ->get('/feature3/data', array_filter([
                'angkatan' => $angkatan,
                'bidang_id' => $bidangId,
            ]))
            ->throw()->json();
    }

    public function feature3Filters(): array
    {
        return $this->client()->get('/feature3/filters')->throw()->json();
    }

    public function match(array $skillIds): array
    {
        return $this->client()
            ->post('/feature4/match', ['skill_ids' => $skillIds])
            ->throw()->json();
    }

    public function status(): array
    {
        return $this->client()->get('/status')->throw()->json();
    }

    public function ingest(UploadedFile $file): array
    {
        return Http::baseUrl(config('services.python.url'))
            ->timeout(120) // proses upload bisa lama
            ->attach('file', file_get_contents($file->getRealPath()), $file->getClientOriginalName())
            ->post('/ingest')
            ->throw()->json();
    }
}