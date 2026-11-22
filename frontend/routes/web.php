<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ControllerFitur1;

Route::get('/', [ControllerFitur1::class, 'hardSkills']);
Route::get('/soft-skills', [ControllerFitur1::class, 'softSkills']);
Route::get('/sertifikasi', [ControllerFitur1::class, 'sertifikasi']);
Route::get('/matriks', [ControllerFitur1::class, 'matriks']);


// Route::get('/', function () {
//     return view('main/hardskill_fitur1');
// });

Route::get('/skill-gap', function () {
    return view('base/fitur2');
});
Route::get('/dashboard-tracer-study', function () {
    return view('base/fitur3');
});
Route::get('/career-navigation', function () {
    return view('base/fitur4');
});
