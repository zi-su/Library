#include "stdafx.h"
#include <iostream>
#include "FileManager.h"

#include <sys/types.h>
#include <sys/stat.h>

int main(int argc, char* argv[]) {
	FileManager::instance()->Load();
	AsyncLoader asyncLoader;
	asyncLoader.StartThread();
	FileInfo fileInfo = FileManager::instance()->GetFileInfo(2006242754);
	void* address = new char[fileInfo.size];
	asyncLoader.LoadRequest(fileInfo, address);

	
	while (true) {
		printf("main thraed\n");

		//メインスレッド中で非同期ロード完了を待ちながら描画？
		Sleep(1);
	}
	return 0;
}