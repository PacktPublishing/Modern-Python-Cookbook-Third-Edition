(*
Python Cookbook, 3rd Ed.

Chapter 14, Application Integration: Combination
Markov Generator
*)
program markov_gen;
uses
    sysUtils,
    Dos;

type
    (* Command-line options. *)
    Options = record
        file_name: String;
        sample_count: Integer;
        randomize: Cardinal;
    end;

    (* The Markov Chain and final outcome state. *)
    Outcome = (InProcess, Success, Fail);
    Chain = record
        target: SmallInt;
        len:  SmallInt;
        sequence:  array of Shortint;
        outcome: Outcome;
    end;

    WriteHeader = procedure(var out: Text; opts: Options; header: Boolean);

    WriteSample = procedure(var out: Text; ch: Chain);

function ProbeValue(): ShortInt;
begin
    Probevalue := Random(6) + Random(6) + 2;
end;

procedure Append(var probe: ShortInt; var ch: Chain);
begin
    SetLength(ch.sequence, ch.len+1);
    ch.sequence[ch.len] := probe;
    ch.len := ch.len + 1;
end;

function Start(probe: ShortInt; var ch: Chain) : Boolean;
begin
    Append(probe, ch);
    case probe of
        7, 11: begin
            ch.outcome := Success;
            ch.target := -1;
            Start := False;
            end;
        2, 3, 12: begin
            ch.outcome := Fail;
            ch.target := -1;
            Start := False;
            end;
    else begin
        ch.outcome := InProcess;
        ch.target := probe;
        Start := True;
        end;
    end;
end;

function GrowUntil(probe: ShortInt; var ch: Chain) : Boolean;
begin
    Append(probe, ch);
    if probe = 7 then begin
        ch.outcome := Fail;
        GrowUntil := False;
        end
    else if probe = ch.target then begin
        ch.outcome := Success;
        GrowUntil := False;
        end
    else
        GrowUntil := True;
end;

function MakeChain: Chain;
var
    ch : Chain;
    continue : Boolean;
    pv : ShortInt;
begin
    SetLength(ch.sequence, 0);
    ch.len := 0;
    pv := ProbeValue();
    continue := Start(pv, ch);
    while continue do begin
        pv := ProbeValue();
        continue := GrowUntil(pv, ch);
        end;
    MakeChain := ch;
end;

procedure ParseArgs(var opts: Options);
var
    param: LongInt;
    option: String;
begin
    opts.sample_count := 100;
    opts.file_name := '';  (* Will write to StdOut. *)
    if GetEnv('RANDOMSEED') <> '' then
        opts.randomize := StrToInt(GetEnv('RANDOMSEED'))
    else
        opts.randomize := 0;
    param := 1;
    while param <= ParamCount do begin
        if ParamStr(param)[1] = '-' then begin
            option := ParamStr(param);
            Delete(option, 1, 1);
            LowerCase(option);
            case option of
                's', '-samples': begin
                    param := param + 1;
                    opts.sample_count := StrToInt(ParamStr(param));
                    end;
                'r', '-randomize': begin
                    param := param + 1;
                    opts.randomize := StrToInt(ParamStr(param));
                    end;
                'o', '-output': begin
                    param := param + 1;
                    opts.file_name := ParamStr(param);
                    end;
                'h', '-help': begin
                    WriteLn('usage: ./markov --samples n --randomize s [output]');
                    WriteLn();
                    WriteLn('Markov Chain Generator');
                    WriteLn();
                    WriteLn('-s --samples n     The number of samples to generate, default is 100.');
                    WriteLn('-r --randomize s   Seed for Random generator.');
                    WriteLn('-o --output name   Ouput file name, default writes to stdout.');
                    WriteLn;
                    WriteLn('Output is a TOML-format file with two tables: Configuration and Samples.');
                    WriteLn('The Samples table is an array of {outcome="...", chain=[...]} mappings.');
                    Halt(1);
                    end;
            else begin
                WriteLn('Invalid option ', ParamStr(param));
                Halt(2);
                end
            end
        end
        else begin
            WriteLn('Invalid positional parameter ', ParamStr(param));
            Halt(2);
        end;
        param := param + 1;
    end;
end;

procedure TOMLWriteHeader(var out: Text; opts: Options; columns: Boolean);
begin
    WriteLn(out, '[Configuration]');
    WriteLn(out, '  file = "', opts.file_name, '"');
    WriteLn(out, '  samples = ', opts.sample_count);
    Writeln(out, '  randomize = ', opts.randomize);
end;

procedure TOMLWriteSample(var out: Text; ch: Chain);
var
    I: Integer;
begin
    WriteLn(out, '[[Samples]]');
    WriteLn(out, '  outcome="', ch.outcome, '"');
    WriteLn(out, '  length=', ch.len);
    Write(out, '  chain=[', ch.sequence[0]);
    For I := 1 to ch.len-1 do
        Write(out, ', ', ch.sequence[I]);
    WriteLn(out, ']');
end;

procedure CSVWriteHeader(var out: Text; opts: Options; columns: Boolean);
begin
    WriteLn(out, '# file = "', opts.file_name, '"');
    WriteLn(out, '# samples = ', opts.sample_count);
    Writeln(out, '# randomize = ', opts.randomize);
    if columns then begin
        Writeln(out, '# -----');
        Writeln(out, 'outcome,length,chain');
    end;
end;

procedure CSVWriteSample(var out: Text; ch: Chain);
var
    I: Integer;
begin
    Write(out, '"', ch.outcome, '"');
    Write(out, ',', ch.len);
    Write(out, ',"', ch.sequence[0]);
    For I := 1 to ch.len-1 do
        Write(out, ';', ch.sequence[I]);
    WriteLn(out, '"');
end;

var
    opts: Options;
    ch: Chain;
    out: Text;
    count: Integer;

    wtrHeader: WriteHeader;
    wtrSample: WriteSample;

begin
    ParseArgs(Opts);

    (* Based on file_filename; default to CSV when writing to StdOut. *)
    if RightStr(opts.file_name, 5) = '.toml' then begin
        wtrHeader := @TOMLWriteHeader;
        wtrSample := @TOMLWriteSample;
    end
    else begin
        wtrHeader := @CSVWriteHeader;
        wtrSample := @CSVWriteSample;
    end;

    if Opts.randomize <> 0 then
        RandSeed := opts.randomize
    else
        Randomize;

    Assign(out, opts.file_name);
    Rewrite(out);

    wtrHeader(out, opts, True);

    for count := 1 to opts.sample_count do begin
        ch := MakeChain();
        wtrSample(out, ch);
    end;

    Close(out);

    if Opts.file_name <> '' then begin
        wtrHeader(StdOut, opts, False);
    end;
end.
