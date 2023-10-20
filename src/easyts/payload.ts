type ReplaceOnce<Search extends string, Replace extends string, Subject extends string> =
    Subject extends `${infer L}${Search}${infer R}` ? `${L}${Replace}${R}` : Subject

type filtered = ReplaceOnce<"flag", "", flag1>;
const a : filtered = false;