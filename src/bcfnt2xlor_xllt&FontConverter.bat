@set str=%~nx1
@set a=%str:~0,-6%
3dsfont\bcfnt2charset %a%.bcfnt %a%.txt
3dsfont\charset2xlor %a%.txt FontConverter\xlor\%a%.xlor
3dsfont\charset2xllt %a%.txt FontConverter\xllt\%a%.xllt
Pause