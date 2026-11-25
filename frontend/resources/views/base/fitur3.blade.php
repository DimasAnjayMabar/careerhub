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

    <div class="mt-6 px-2">
        @yield('dashboard-content')
    </div>
@endsection
