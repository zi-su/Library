#pragma once

#include "stdafx.h"

struct FileInfo {
	char path[PATH_MAX];
	uint32_t size;
	uint32_t fileid;
};

struct LoadData {
	FileInfo fileInfo;
	void* dstAddress;
};

//FileInfo���Ǘ�����N���X
class FileManager {
public:
	friend class AsyncLoadThread;
	FileManager();
	~FileManager();

	FileInfo& GetFileInfo(uint32_t fileid);
	//FileInfo��ǂݍ���
	void Load();
	static FileManager* instance() {
		static FileManager instance;
		return &instance;
	}
private:
	//FileInfo�̃n�b�V�����L�[�Ɏ��ԂɃA�N�Z�X
	std::unordered_map<uint32_t, FileInfo> fileInfoMap;
};

//�񓯊��t�@�C�����[�h���Ǘ�
class AsyncLoader {
public:
	AsyncLoader() = default;
	~AsyncLoader() = default;

	//�񓯊����[�h�̃X���b�h�N��
	void StartThread();

	//�񓯊����[�h�I���҂�
	void Join();

	//���[�h���N�G�X�g�B�Ώۂ̃t�@�C���C���t�H�A���[�h��A�h���X
	void LoadRequest(FileInfo fileInfo, void* dstAddress);

	bool IsEmpty();
	LoadData Pop();
private:
	//���[�h�Ώۂ����߂�L���[
	std::queue<LoadData> loadQueue;
	std::atomic<bool> threadFinish;
	//�񓯊����[�h�X���b�h
	std::thread asyncLoadThread;

	
};