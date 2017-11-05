#include "stdafx.h"
#include "FileManager.h"

namespace {
	std::mutex loadMutex;

	void AsyncLoadThreadFunc(AsyncLoader* loader) {
		//�񓯊����[�h�֐�
		while (true) {
			//���[�h���N�G�X�g������Ă邩
			loadMutex.lock();
			//�L���[������o���ă��[�h�����s
			if (!loader->IsEmpty()) {
				LoadData loadData = loader->Pop();
				loadMutex.unlock();
				FileInfo fileInfo = loadData.fileInfo;
				printf("asyncLoadStart %s\n", fileInfo.path);
				//�������m�ۂ́H���[�h���N�G�X�g�O�Ɋm�ۂ��ēǍ���Ƃ��ēn���Ă���
				FILE* fp = nullptr;

				if (fopen_s(&fp, fileInfo.path, "rb") == 0) {
					
					fread(loadData.dstAddress, fileInfo.size, 1, fp);

					fclose(fp);
					printf("asyncLoadEnd %s\n", fileInfo.path);
				}
				else {
					assert(false);
				}
			}
			else {
				//�L���[����ɂȂ��Ă�����
				loadMutex.unlock();
				Sleep(1);
			}
			//�X���b�h�I���t���O�`�F�b�N
			Sleep(1);
		}
	}
}

/*
�t�@�C���}�l�[�W���[
*/
FileManager::FileManager() {

}

FileManager::~FileManager() {

}

FileInfo& FileManager::GetFileInfo(uint32_t fileid) {
	assert(fileInfoMap.find(fileid) != fileInfoMap.end());

	return fileInfoMap[fileid];
}
void FileManager::Load() {
	FILE* fp = nullptr;
	auto ferr = fopen_s(&fp, "fileinfo.bin", "rb");
	struct _stat buf;
	int result = _stat("fileinfo.bin", &buf);
	if (result == 0)
	{
		printf("stat :%ld\n", buf.st_size);
	}
	void* cbuf = new char[buf.st_size];
	size_t read_size = fread((void*)cbuf, buf.st_size, 1, fp);
	auto num = buf.st_size / sizeof(FileInfo);
	FileInfo* fileInfo = static_cast<FileInfo*>(cbuf);
	for (unsigned int i = 0; i < num; i++) {
		FileInfo info = fileInfo[i];
		fileInfoMap[info.fileid] = info;
	}
}

/*
�񓯊����[�h
*/
void AsyncLoader::StartThread() {
	asyncLoadThread = std::thread(AsyncLoadThreadFunc, this);
}

void AsyncLoader::Join() {
	asyncLoadThread.join();
}

void AsyncLoader::LoadRequest(FileInfo fileInfo, void* dstAddress) {
	std::lock_guard<std::mutex> guard(loadMutex);
	LoadData data;
	data.fileInfo = fileInfo;
	data.dstAddress = dstAddress;
	loadQueue.push(data);
}

LoadData AsyncLoader::Pop() {
	LoadData loadData = loadQueue.front();
	loadQueue.pop();
	return loadData;
}

bool AsyncLoader::IsEmpty() {
	return loadQueue.empty();
}