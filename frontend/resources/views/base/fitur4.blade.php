@extends('base.app')

@section('header_title', 'Career Navigation System')

@section('content')
    <!-- Navigasi Tab -->
    @php
        $isMatcher = request()->route('tab') === 'matcher';
    @endphp

    <!-- deskripsi -->
    <div class="flex mb-10 gap-2">
        <svg class="w-5 h-5 shrink-0" fill="none" stroke="#6A7282" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
        </svg>

        <span class="text-sm text-gray-500">Cari dan Temukan Karirmu Dari Skill-Skill Yang Ada</span>   
    </div>

    <!--  -->
    <nav class="grid grid-cols-2 gap-4 border-b border-gray-200">
        <!-- Career Explorer -->
        <div class="pb-2 border-b-2 {{ !$isMatcher ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/career-navigation"
                class="block px-4 py-2 text-center rounded-lg font-medium transition
                {{ !$isMatcher ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Career Explorer
            </a>
        </div>

        <!-- Career Matcher -->
        <div class="pb-2 border-b-2 {{ $isMatcher ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/career-navigation/matcher"
                class="block px-4 py-2 text-center rounded-lg font-medium transition
                {{ $isMatcher ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Ayo Navigasi Karirmu 🚀
            </a>
        </div>

    </nav>

    <div class="mt-6 px-2">
        @yield('karir-explore-content')
        @yield('navigasi-karir-content')
    </div>


@endsection