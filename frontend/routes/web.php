<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ControllerFitur1;
use App\Http\Controllers\ControllerFitur2;

// Fitur 1
Route::get('/', [ControllerFitur1::class, 'hardSkills']);
Route::get('/soft-skills', [ControllerFitur1::class, 'softSkills']);
Route::get('/sertifikasi', [ControllerFitur1::class, 'sertifikasi']);
Route::get('/matriks', [ControllerFitur1::class, 'matriks']);

// Fitur 2
Route::get('/skill-gap', [ControllerFitur2::class, 'skillGap']);
Route::get('/dibutuhkan-dirasakurang', [ControllerFitur2::class, 'dibutuhkanVsTidakDisebut']);
Route::get('/tren-angkatan', [ControllerFitur2::class, 'tren']);
Route::get('/waktu-tunggu', [ControllerFitur2::class, 'waktuTunggu']);


Route::get('/dashboard-tracer-study', function () {
    return view('base/fitur3');
});
Route::get('/career-navigation', function () {
    return view('base/fitur4');
});
Route::get('/master-data', function () {
    return view('base/upload');
});
