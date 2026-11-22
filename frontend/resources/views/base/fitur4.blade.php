@extends('base.app')

@section('header_title', 'Career Navigation System')

@section('content')
    <div class="flex flex-col">
        <p class="text-md text-gray-700 mb-8">Agregasi kompetensi yang benar-benar dibutuhkan alumni di bidang pekerjaannya</p>   
    </div>

    <!--  -->
    <nav class="grid grid-cols-2 gap-4 border-b border-gray-200">

        <div class="pb-2 border-b-2 {{ request()->is('/') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('/') ? ' text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Career Explorer
            </a>
        </div>

        <div class="pb-2 border-b-2 {{ request()->is('soft-skills*') ? 'border-[#1E3A8A]' : 'border-transparent' }}">
            <a href="/soft-skills"
                class="block px-4 py-2 text-center rounded-lg font-medium transition {{ request()->is('/soft-skills') ? 'text-[#1E3A8A]' : 'text-gray-700 hover:bg-[#2B72D6]/10 hover:text-[#2B72D6]' }}">
                Ayo Navigasi Karirmu🚀
            </a>
        </div>
    </nav>


@endsection