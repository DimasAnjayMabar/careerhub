@extends('base.app')

@section('header_title', 'Dashboard Tracer Study')

@section('content')
    <!-- deskripsi -->
    <div class="flex mb-12 gap-2">
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="#6A7282" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
        </svg>

        <span class="text-sm text-gray-500">Gunakan Filter Dibawah Ini Untuk Mengeksplorasi Data</span>   
    </div>

    <!-- Filter -->
    <div class="flex border border-gray-200 rounded-lg w w-full">
        <svg class="w-6 h-6 shrink-0" fill="none" stroke="#1E3A8A" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>

        <span class="text-[#0F294A] text-xl font-semibold ml-2">Filter Global</span>

    </div>
@endsection
