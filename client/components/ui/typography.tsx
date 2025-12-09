function TypographyH1({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <h1 className="text-4xl font-semibold font-display md:text-5xl text-foreground scroll-m-20 text-left tracking-tight text-balance">
      {children}
    </h1>
  );
}

function TypographyP({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <p className="leading-7 not-first:mt-6">{children}</p>;
}

function TypographyMuted({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <p className="text-muted-foreground text-sm">{children}</p>;
}

export { TypographyH1, TypographyP, TypographyMuted };
