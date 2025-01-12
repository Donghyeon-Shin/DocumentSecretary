<%*
	const dv = app.plugins.plugins["dataview"].api;
	const openPublishPanel = app.commands.commands["publish:view-changes"].callback;
	const FileName = "Book Introduction";
	const tFile = tp.file.find_tfile(FileName);
	
// Major DataView Query
	const MajorQuery = `table ("![|100](" + cover_url + ")") as 표지, author as 지은이, total_page as 분량, tags, status as 상태, my_rate as 평점 from "Study/Book/Book Content/Major/Books"`;
	const MajorQueryOutput = await dv.queryMarkdown(MajorQuery);
	
// Novel DataView Query
	const NovelQuery = `table ("![|100](" + cover_url + ")") as 표지, author as 지은이, total_page as 분량, tags, status as 상태, my_rate as 평점
from "Study/Book/Book Content/Novel/Books"`;
	const NovelQueryOutput = await dv.queryMarkdown(NovelQuery);

// Humanities DataView Query
	const HumanitiesQuery = `table ("![|100](" + cover_url + ")") as 표지, author as 지은이, total_page as 분량, tags, status as 상태, my_rate as 평점
from "Study/Book/Book Content/Humanities/Books"`;
	const HumanitiesQueryOutput = await dv.queryMarkdown(HumanitiesQuery);

// Content Before/After Table

	const ContentBeforeDataView = "# Meaning of Reading\n책은 자신만의 호흡으로 읽기 때문에 다른 매체와 다르게 상대적으로 스스로 생각해볼 수 있는 시간이 많다. 이러한 시간은 전문 서적에서 복잡하고 어려운 내용이 나왔을 때 잠시 멈추어 생각을 정리해볼 수 있게 해주고, 소설을 읽으며 주인공이 느끼는 감정이 무엇인지 판단이 서지 않을 때는 비슷한 상황을 상상하며 주인공의 감정에 이입할 수 있게 해주기도 한다. 이러한 호흡 덕분에 다른 매체들보다 장기 기억에 남는 정보량도 더 많다. 어릴 때 죽어도 하기 싫은 독서가 지금와서 재밌어진 이유도 빠른 호흡을 강요하는 강제 독서에서 벗어나 나만의 호흡으로 읽는 독서를 맛보았기 때문이지 않을까 싶다.\n# Reading record\n- Book Part은 2023.01.09일부터의 책 기록 보관서이다.\n- 읽은 책, 읽고 있는 책, 읽다가 도중에 포기한 책도 적혀있다.\n- Major과 Novel, Humanities으로 나누어져 있으며 내 전공은 아니어도 내 전공에 도움이 된 책들은 Major Part에 포함되어 있다.\n- 세부 내용으로 평점, 상태, 읽은 기간, 감상평이 담겨져있다."

	const ContentAfterDataView = ""

	// write query output to file
  const fileContent = `${ContentBeforeDataView} \n## Major\n\n${MajorQueryOutput.value} \n## Novel\n\n${NovelQueryOutput.value}\n## Humanities\n\n${HumanitiesQueryOutput.value}\n${ContentAfterDataView}`;
  try {
    await app.vault.modify(tFile, fileContent);
    new Notice(`Updated ${tFile.basename}.`);
  } catch (error) {
    new Notice("⚠️ ERROR updating! Check console. Skipped file: " + FileName , 0);
  }
%>