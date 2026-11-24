@extends('base.app')

@section('header_title', 'Master Data')

@section('content')
    <!-- deskripsi -->
    <div class="flex mb-10 gap-2">
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="#6A7282" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
        </svg>

        <span class="text-sm text-gray-500">Upload Data Untuk Melihat dan Mengakses Informasi terbaru</span>   
    </div>

    <!-- button upload -->
    <div class="justify-items-end gap-4 mb-6">
        <!-- <div class="">
            <a href="/upload"
                class="flex items-center px-6 py-2 gap-2 font-medium rounded-lg bg-red-500 text-white shadow-sm' : 'text-gray-700 hover:bg-red-700 hover:text-[#1E3A8A]' }}">
                <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                <span>Lihat Data</span>
            </a>
        </div> -->
        <div class="">
            <a href="/upload"
                class="flex items-center px-6 py-2 gap-2 font-medium rounded-lg bg-[#1E3A8A] text-white shadow-sm' : 'text-gray-700 hover:bg-[#0F294A] hover:text-[#1E3A8A]' }}">
                <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
                </svg>

                <span>Upload</span>
            </a>
        </div>
    </div>

    <!-- data saat ini -->
    <div class="border border-gray-200 rounded-lg mb-8">
        <div class="px-4 py-4">
            <h1 class="text-xl font-semibold mb-4">Data Saat Ini</h1>
            
            <div class="flex gap-2 items-center">
                <svg class="w-7 h-7 shrink-0" fill="none" stroke="#6A7282" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>

                <span class="text-gray-400">contohdata.xlx</span>
                <span class="text-gray-400 ml-8">Last Upload: 20/11/2026</span>
            </div>
        </div>

    </div>


@endsection