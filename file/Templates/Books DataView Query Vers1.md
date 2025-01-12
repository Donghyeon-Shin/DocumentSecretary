<%*
	const dv = app.plugins.plugins["dataview"].api;
	const openPublishPanel = app.commands.commands["publish:view-changes"].callback;

	const MajorFileName = "Major Information";
	const MajorQuery = `table ("![|100](" + cover_url + ")") as 표지, author as 지은이, total_page as 분량, tags, status as 상태, my_rate as 평점
from "Study/Book/Book Content/Major/Books"`;
	const tMajorFile = tp.file.find_tfile(MajorFileName);
	const MajorQueryOutput = await dv.queryMarkdown(MajorQuery);
	// write query output to file
	await app.vault.modify(tMajorFile, MajorQueryOutput.value);

	const NovelFileName = "Novel Information";
	const NovelQuery = `table ("![|100](" + cover_url + ")") as 표지, author as 지은이, total_page as 분량, tags, status as 상태, my_rate as 평점
from "Study/Book/Book Content/Novel/Books"`;
	const tNovelFile = tp.file.find_tfile(NovelFileName);
	const NovelQueryOutput = await dv.queryMarkdown(NovelQuery);
	// write query output to file
	await app.vault.modify(tNovelFile, NovelQueryOutput.value);
	
	const HumanitiesFileName = "Humanities Information";
	const HumanitiesQuery = `table ("![|100](" + cover_url + ")") as 표지, author as 지은이, total_page as 분량, tags, status as 상태, my_rate as 평점
from "Study/Book/Book Content/Humanities/Books"`;
	const tHumanitiesFile = tp.file.find_tfile(HumanitiesFileName);
	const HumanitiesQueryOutput = await dv.queryMarkdown(HumanitiesQuery);
	// write query output to file
	await app.vault.modify(tHumanitiesFile, HumanitiesQueryOutput.value);
%>

