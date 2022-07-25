<?php

interface ApiRequesterI
{
    public function __construct(HelloSignSDK\Configuration $config);

    public function run(
        array $parameters,
        array $data,
        array $files
    ): array;
}
