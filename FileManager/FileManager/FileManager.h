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

//FileInfoを管理するクラス
class FileManager {
public:
	friend class AsyncLoadThread;
	FileManager();
	~FileManager();

	FileInfo& GetFileInfo(uint32_t fileid);
	//FileInfoを読み込む
	void Load();
	static FileManager* instance() {
		static FileManager instance;
		return &instance;
	}
private:
	//FileInfoのハッシュをキーに実態にアクセス
	std::unordered_map<uint32_t, FileInfo> fileInfoMap;
};

//非同期ファイルロードを管理
class AsyncLoader {
public:
	AsyncLoader() = default;
	~AsyncLoader() = default;

	//非同期ロードのスレッド起動
	void StartThread();

	//非同期ロード終了待ち
	void Join();

	//ロードリクエスト。対象のファイルインフォ、ロード先アドレス
	void LoadRequest(FileInfo fileInfo, void* dstAddress);

	bool IsEmpty();
	LoadData Pop();
private:
	//ロード対象をためるキュー
	std::queue<LoadData> loadQueue;
	std::atomic<bool> threadFinish;
	//非同期ロードスレッド
	std::thread asyncLoadThread;

	
};