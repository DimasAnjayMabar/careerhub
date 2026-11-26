<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ControllerFitur1;
use App\Http\Controllers\ControllerFitur2;
use App\Http\Controllers\ControllerFitur3;
use App\Http\Controllers\ControllerFitur4;
use App\Http\Controllers\ControllerUpload;

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

// Fitur 3
Route::get('/dashboard-tracer-study', [ControllerFitur3::class, 'dashboard']);

// Fitur 4
Route::get('/career-navigation/{tab?}', [ControllerFitur4::class, 'careerNavigation'])->where('tab', 'matcher');;
Route::post('/career-navigation/match', [ControllerFitur4::class, 'match']);

// Upload
// Route::get('/master-data', [ControllerUpload::class, 'index'])->name('master-data.index');
Route::get('/master-data', [ControllerUpload::class, 'index'])->name('base.upload.index');
Route::post('/master-data/upload', [ControllerUpload::class, 'upload'])->name('base.upload');
Route::delete('/master-data', [ControllerUpload::class, 'destroy'])->name('base.upload.destroy');

// Route::get('/master-data', function () {
//     return view('base/upload');
// });
